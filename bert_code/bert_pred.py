import pandas as pd
import numpy as np
from transformers import BertTokenizerFast, TFBertForTokenClassification
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
import tensorflow as tf

# 讀入模型和 tokenizer
checkpoint_path='D:/aicup/class_word_weigh/bio_bert_0608_2'
tag2id={'B-AGE': 0,
 'B-CITY': 1,
 'B-COUNTRY': 2,
 'B-COUNTY': 3,
 'B-DATE': 4,
 'B-DEPARTMENT': 5,
 'B-DISTRICT': 6,
 'B-DOCTOR': 7,
 'B-DURATION': 8,
 'B-FAMILYNAME': 9,
 'B-FAX': 10,
 'B-HEALTH_PLAN_NUMBER': 11,
 'B-HOSPITAL': 12,
 'B-ID_NUMBER': 13,
 'B-IPADDRESS': 14,
 'B-LOCATION-OTHER': 15,
 'B-MEDICAL_RECORD_NUMBER': 16,
 'B-ORGANIZATION': 17,
 'B-PATIENT': 18,
 'B-PERSONALNAME': 19,
 'B-PHONE': 20,
 'B-PROFESSION': 21,
 'B-ROOM': 22,
 'B-SET': 23,
 'B-SOCIAL_SECURITY_NUMBER': 24,
 'B-STATE': 25,
 'B-STREET': 26,
 'B-TIME': 27,
 'B-URL': 28,
 'B-ZIP': 29,
 'I-AGE': 30,
 'I-CITY': 31,
 'I-COUNTRY': 32,
 'I-COUNTY': 33,
 'I-DATE': 34,
 'I-DEPARTMENT': 35,
 'I-DISTRICT': 36,
 'I-DOCTOR': 37,
 'I-DURATION': 38,
 'I-FAMILYNAME': 39,
 'I-FAX': 40,
 'I-HEALTH_PLAN_NUMBER': 41,
 'I-HOSPITAL': 42,
 'I-ID_NUMBER': 43,
 'I-IPADDRESS': 44,
 'I-LOCATION-OTHER': 45,
 'I-MEDICAL_RECORD_NUMBER': 46,
 'I-ORGANIZATION': 47,
 'I-PATIENT': 48,
 'I-PERSONALNAME': 49,
 'I-PHONE': 50,
 'I-PROFESSION': 51,
 'I-ROOM': 52,
 'I-SET': 53,
 'I-SOCIAL_SECURITY_NUMBER': 54,
 'I-STATE': 55,
 'I-STREET': 56,
 'I-TIME': 57,
 'I-URL': 58,
 'I-ZIP': 59,
 'o': 60}

id2tag={0: 'B-AGE',
 1: 'B-CITY',
 2: 'B-COUNTRY',
 3: 'B-COUNTY',
 4: 'B-DATE',
 5: 'B-DEPARTMENT',
 6: 'B-DISTRICT',
 7: 'B-DOCTOR',
 8: 'B-DURATION',
 9: 'B-FAMILYNAME',
 10: 'B-FAX',
 11: 'B-HEALTH_PLAN_NUMBER',
 12: 'B-HOSPITAL',
 13: 'B-ID_NUMBER',
 14: 'B-IPADDRESS',
 15: 'B-LOCATION-OTHER',
 16: 'B-MEDICAL_RECORD_NUMBER',
 17: 'B-ORGANIZATION',
 18: 'B-PATIENT',
 19: 'B-PERSONALNAME',
 20: 'B-PHONE',
 21: 'B-PROFESSION',
 22: 'B-ROOM',
 23: 'B-SET',
 24: 'B-SOCIAL_SECURITY_NUMBER',
 25: 'B-STATE',
 26: 'B-STREET',
 27: 'B-TIME',
 28: 'B-URL',
 29: 'B-ZIP',
 30: 'I-AGE',
 31: 'I-CITY',
 32: 'I-COUNTRY',
 33: 'I-COUNTY',
 34: 'I-DATE',
 35: 'I-DEPARTMENT',
 36: 'I-DISTRICT',
 37: 'I-DOCTOR',
 38: 'I-DURATION',
 39: 'I-FAMILYNAME',
 40: 'I-FAX',
 41: 'I-HEALTH_PLAN_NUMBER',
 42: 'I-HOSPITAL',
 43: 'I-ID_NUMBER',
 44: 'I-IPADDRESS',
 45: 'I-LOCATION-OTHER',
 46: 'I-MEDICAL_RECORD_NUMBER',
 47: 'I-ORGANIZATION',
 48: 'I-PATIENT',
 49: 'I-PERSONALNAME',
 50: 'I-PHONE',
 51: 'I-PROFESSION',
 52: 'I-ROOM',
 53: 'I-SET',
 54: 'I-SOCIAL_SECURITY_NUMBER',
 55: 'I-STATE',
 56: 'I-STREET',
 57: 'I-TIME',
 58: 'I-URL',
 59: 'I-ZIP',
 60: 'o'}
model = TFBertForTokenClassification.from_pretrained("bert-base-multilingual-cased", num_labels=len(tag2id))
optimizer = Adam(learning_rate=1e-5)
model.compile(optimizer=optimizer, metrics=["accuracy"])
model.load_weights(checkpoint_path) # 或用 model.save_pretrained/load_pretrained
tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
# tag2id={'B-AGE': 0, 'B-CITY': 1, 'B-COUNTRY': 2, 'B-COUNTY': 3, 'B-DATE': 4, 'B-DEPARTMENT': 5, 'B-DISTRICT': 6, 'B-DOCTOR': 7, 'B-DURATION': 8, 'B-FAMILYNAME': 9, 'B-HOSPITAL': 10, 'B-ID_NUMBER': 11, 'B-LOCATION-OTHER': 12, 'B-MEDICAL_RECORD_NUMBER': 13, 'B-ORGANIZATION': 14, 'B-PATIENT': 15, 'B-PERSONALNAME': 16, 'B-PHONE': 17, 'B-PROFESSION': 18, 'B-SET': 19, 'B-STATE': 20, 'B-STREET': 21, 'B-TIME': 22, 'B-URL': 23, 'B-ZIP': 24, 'I-AGE': 25, 'I-CITY': 26, 'I-COUNTY': 27, 'I-DATE': 28, 'I-DEPARTMENT': 29, 'I-DOCTOR': 30, 'I-DURATION': 31, 'I-HOSPITAL': 32, 'I-ID_NUMBER': 33, 'I-LOCATION-OTHER': 34, 'I-MEDICAL_RECORD_NUMBER': 35, 'I-ORGANIZATION': 36, 'I-PATIENT': 37, 'I-PERSONALNAME': 38, 'I-PROFESSION': 39, 'I-SET': 40, 'I-STATE': 41, 'I-STREET': 42, 'I-TIME': 43, 'I-URL': 44, 'I-ZIP': 45, 'o': 46}
def predict_tags(text_tokens):
    encoding = tokenizer(text_tokens,
                         is_split_into_words=True,
                         return_tensors="tf",
                         truncation=True,
                         padding='max_length',
                         max_length=128)
    
    outputs = model(encoding)
    predictions = tf.argmax(outputs.logits, axis=-1).numpy()[0]
    word_ids = encoding.word_ids(batch_index=0)

    decoded_tags = []
    previous_word_idx = None
    for i, word_idx in enumerate(word_ids):
        if word_idx is None:
            continue
        elif word_idx != previous_word_idx:
            decoded_tags.append(id2tag[predictions[i]])
        previous_word_idx = word_idx

    return decoded_tags

# %%
import json
import os
# D:\aicup\task2_test\task2_json
# jason_path="D:/aicup/task2_test/task2_json/"
jason_path=r"D:/aicup/private_result_AI_CUP/task2_json_all/"
jason_flie=os.listdir(jason_path)
save_txt=open("bert_code/bert_data/bert/task2_test_ans0608_2.txt", "w")
for ttt in range(len(jason_flie)):
    
    jason_path_file=jason_path+jason_flie[ttt]
    with open(jason_path_file, 'r') as f:
        data = json.load(f)
    text_list=[]
    time_list=[]
    txt_list=[]
    for i in data:
        a=i["words"]
        # print(a)
        for j in a:
            try:
                time_list.append([j['start'],j['end']])
                text_list.append(j['word'])
            except:
                pass
                # text_list.append(j['word'])
                # time_list.append(["0","0"])
    text_token_list=[]
    time_token_list=[]         
    for itext in range(len(text_list)):
        
        word_text = tokenizer.tokenize(text_list[itext])
        for itime in range(len(word_text)):
            text_token_list.append(word_text[itime])
            time_token_list.append(time_list[itext])

    bio_tags = predict_tags(text_token_list)
    for text11, tag ,time in zip(text_token_list, bio_tags,time_token_list):
        if tag=="o":
            pass
        else:
            ans_list=[jason_flie[ttt][:-5],"\t",tag,"\t",time[0],"\t",time[1],"\t",text11,"\n"]
            txt_list.append(ans_list)
            
    def merge_bio_entities(data):
        merged = []
        i = 0
        while i < len(data):
            row = data[i]
            tag = str(row[2]).strip()
    
            if tag.startswith("B-"):
                current_type = tag[2:]
                try:
                    start_time = str(row[4])
                    end_time = str(row[6])
                except ValueError:
                    i += 1
                    continue
    
                entity_tokens = [str(row[8]).strip()]
    
                j = i + 1
                while j < len(data):
                    next_tag = str(data[j][2]).strip()
                    if next_tag.startswith("I-"):
                        try:
                            end_time = str(data[j][6])
                            entity_tokens.append(str(data[j][8]).strip())
                        except ValueError:
                            break
                        j += 1
                    else:
                        break
    
                merged.append([
                    row[0],                     # ID
                    '\t',
                    current_type.upper(),      # 去掉 B-/I-
                    '\t',
                    start_time,
                    '\t',
                    end_time,
                    '\t',
                    ' '.join(entity_tokens),   # 合併 token
                    '\n'
                ])
                i = j
            else:
                i += 1
    
        return merged
    fixed_result = merge_bio_entities(txt_list)
    for row in fixed_result:
        save_txt.writelines(row)
        # print(entry)
        
save_txt.close()