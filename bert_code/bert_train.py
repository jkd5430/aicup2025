import pandas as pd
import numpy as np
from transformers import BertTokenizerFast, TFBertForTokenClassification
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf
import ast


dfaug = pd.read_csv("bert_code/bert_data/bert/task2_aug.txt", sep="\t", header=None, names=["id", "tokens", "labels"])
dfaug["tokens"] = dfaug["tokens"].apply(ast.literal_eval)
dfaug["labels"] = dfaug["labels"].apply(ast.literal_eval)

# 把 "O" 改成 "o"
dfaug["labels"] = dfaug["labels"].apply(lambda labels: [label.lower() if label == "O" else label for label in labels])

# 找出 tokens 和 labels 長度不一致的資料
mismatch_df = dfaug[dfaug["tokens"].str.len() != dfaug["labels"].str.len()]
dfaug = dfaug.drop(index=mismatch_df.index).reset_index(drop=True)


df1 = pd.read_csv("bert_code/bert_data/bert/class_01_bio.txt", sep="\t", header=None, names=["id", "tokens", "labels", "entity_types", "entity_texts", "extra1", "extra2"])
df1_mu = pd.read_csv("bert_code/bert_data/bert/class_01_mu_bio.txt", sep="\t", header=None, names=["id", "tokens", "labels", "entity_types", "entity_texts", "extra1", "extra2"])
df2 = pd.read_csv("bert_code/bert_data/bert/class_02_bio.txt", sep="\t", header=None, names=["id", "tokens", "labels", "entity_types", "entity_texts", "extra1", "extra2"])
df2_mu = pd.read_csv("bert_code/bert_data/bert/class_02_mu_bio.txt", sep="\t", header=None, names=["id", "tokens", "labels", "entity_types", "entity_texts", "extra1", "extra2"])
dfval = pd.read_csv("bert_code/bert_data/bert/class_val_bio.txt", sep="\t", header=None, names=["id", "tokens", "labels", "entity_types", "entity_texts", "extra1", "extra2"])
dfval_mu = pd.read_csv("bert_code/bert_data/bert/class_val_mu_bio.txt", sep="\t", header=None, names=["id", "tokens", "labels", "entity_types", "entity_texts", "extra1", "extra2"])
df2ch = pd.read_csv("bert_code/bert_data/bert/class_02_ch_bio.txt", sep="\t", header=None, names=["id", "tokens", "labels", "entity_types", "entity_texts", "extra1", "extra2"])

# 合併兩份資料
df = pd.concat([df1, df2,dfaug,df1_mu,df2_mu], ignore_index=True)
dfval = pd.concat([dfval,dfval_mu,df2ch], ignore_index=True)

# 解析字串格式為實際 list
df["tokens"] = df["tokens"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
df["labels"] = df["labels"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

dfval["tokens"] = dfval["tokens"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
dfval["labels"] = dfval["labels"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
# 取得所有標籤種類
dfall = pd.concat([df], ignore_index=True)

unique_tags = sorted({tag for tags in dfall["labels"] for tag in tags})


tag2id = {tag: idx for idx, tag in enumerate(unique_tags)}
id2tag = {idx: tag for tag, idx in tag2id.items()}

# === tokenizer ===
tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
MAX_LEN = 128

def encode_examples(tokens_list, labels_list):
    input_ids, attention_masks, label_ids = [], [], []
    for tokens, labels in zip(tokens_list, labels_list):
        encoding = tokenizer(tokens,
                             is_split_into_words=True,
                             truncation=True,
                             padding='max_length',
                             max_length=MAX_LEN,
                             return_tensors="np")
        word_ids = encoding.word_ids(batch_index=0)
        label_id = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                label_id.append(-100)
            elif word_idx != previous_word_idx:
                label_id.append(tag2id[labels[word_idx]])
            else:
                label_id.append(tag2id[labels[word_idx]] if labels[word_idx].startswith("I-") else -100)
            previous_word_idx = word_idx
        input_ids.append(encoding["input_ids"][0])
        attention_masks.append(encoding["attention_mask"][0])
        label_ids.append(label_id)
    return {
        "input_ids": np.array(input_ids),
        "attention_mask": np.array(attention_masks),
        "labels": np.array(label_ids)
    }

# === 編碼資料 ===
train_texts = df["tokens"]
train_labels = df["labels"]
val_texts = dfval["tokens"]
val_labels= dfval["labels"]
train_data = encode_examples(train_texts.tolist(), train_labels.tolist())
val_data = encode_examples(val_texts.tolist(), val_labels.tolist())

# train_texts, val_texts, train_labels, val_labels = train_test_split(df["tokens"], df["labels"], test_size=0.1, random_state=42)
# train_data = encode_examples(train_texts.tolist(), train_labels.tolist())
# val_data = encode_examples(val_texts.tolist(), val_labels.tolist())

import tensorflow as tf
from tensorflow.keras.losses import Loss

class FocalLossWithIgnore(Loss):
    def __init__(self, gamma=2.0, alpha=0.25, ignore_index=-100, **kwargs):
        super().__init__(**kwargs)
        self.gamma = gamma
        self.alpha = alpha
        self.ignore_index = ignore_index

    @tf.autograph.experimental.do_not_convert
    def call(self, y_true, y_pred):
        y_true = tf.cast(y_true, tf.int32)
        mask = tf.not_equal(y_true, self.ignore_index)

        # Flatten and mask
        mask_flat = tf.reshape(mask, [-1])
        y_true_flat = tf.reshape(y_true, [-1])
        y_pred_flat = tf.reshape(y_pred, [-1, tf.shape(y_pred)[-1]])

        y_true_masked = tf.boolean_mask(y_true_flat, mask_flat)
        y_pred_masked = tf.boolean_mask(y_pred_flat, mask_flat)

        y_true_one_hot = tf.one_hot(y_true_masked, depth=tf.shape(y_pred)[-1])
        y_pred_softmax = tf.nn.softmax(y_pred_masked, axis=-1)

        pt = tf.reduce_sum(y_true_one_hot * y_pred_softmax, axis=-1)
        loss = -self.alpha * tf.pow(1.0 - pt, self.gamma) * tf.math.log(tf.clip_by_value(pt, 1e-9, 1.0))
        return tf.reduce_mean(loss)

# %%


focal_loss = FocalLossWithIgnore(gamma=2.0, alpha=0.25)

# === 模型構建 ===
model = TFBertForTokenClassification.from_pretrained("bert-base-multilingual-cased", num_labels=len(tag2id))

optimizer = Adam(learning_rate=1e-5)
model.compile(optimizer=optimizer, loss=focal_loss,metrics=["accuracy"])
# === 模型訓練 ===
checkpoint_path='D:/aicup/class_word_weigh/bio_bert_0608'

checkpoint = ModelCheckpoint(checkpoint_path, monitor="val_loss", save_best_only=True,save_weights_only=True)
history =model.fit(
    x={"input_ids": train_data["input_ids"], "attention_mask": train_data["attention_mask"]},
    y=train_data["labels"],
    validation_data=(
        {"input_ids": val_data["input_ids"], "attention_mask": val_data["attention_mask"]},
        val_data["labels"]
    ),
    epochs=20,
    batch_size=32,
    callbacks=[checkpoint]
)
import matplotlib.pyplot as plt

# 畫 Loss 曲線
plt.figure()
plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Val Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training and Validation Loss")
plt.legend()
plt.grid(True)
plt.show()