import pandas as pd
import json
from word2number import w2n
import re
from transformers import BertTokenizerFast

def convert_token(token):
    try:
        return str(w2n.word_to_num(token))
    except ValueError:
        return token
# # df1 = pd.read_csv()
ann_df = pd.read_csv("bert_code/bert_data/task2_02_answer_ch.txt" , sep="\t", header=None,)
# ann_df = pd.read_csv("bert_code/bert_data/task2_01_answer.txt"  , sep="\t", header=None,)
# ann_df = pd.read_csv("bert_code/bert_data/task2_val_answer.txt" , sep="\t", header=None,)
ann_un=ann_df[0].unique()
ann_un=ann_un.tolist()
bio_txt = open("bert_code/bert_data/bert/class_02_ch_bio.txt", "w", encoding="utf-8")

word_df = pd.read_csv("bert_code/bert_data/task1_02_answer_ch.txt" , sep="\t", header=None,)
# word_df = pd.read_csv("bert_code/bert_data/task1_01_answer.txt" , sep="\t", header=None,)
# word_df = pd.read_csv("bert_code/bert_data/task1_val_answer.txt" , sep="\t", header=None,)
tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")


for i in range(len(word_df)):
    tag_list=[]
    notfind_tag_list=[]
    text_list=[]
    notfind_text_list=[]
    shi_labble=[0]*8
    labble=0
    a=word_df.iloc[i, 1]
    try:
        ann_un.index(word_df.iloc[i, 0])
        ann=1
    except:
        ann=0
    if ann==1:
        tag_sem=ann_df[ann_df[0]==ann_un[ann_un.index(word_df.iloc[i, 0])]]
        word_text=a.lower()
        word_text = tokenizer.tokenize(word_text)
        word_text_2n = [convert_token(token) for token in word_text]
        bio_labble=["o"]*len(word_text_2n)
        for j in range(len(tag_sem)):
            tag_sem_tag=tag_sem.iloc[j, 1]
            tag_sem_con=tag_sem.iloc[j, 4]
            tag_sem_con=tag_sem_con.lower()
            tag_sem_con = tokenizer.tokenize(tag_sem_con)
            bio_tag=["I-"+str(tag_sem_tag)]*len(tag_sem_con)
            bio_tag[0]="B-"+str(tag_sem_tag)
            tag_sem_con_2n = [convert_token(token_tag) for token_tag in tag_sem_con]
            found = False
            for k in range(len(word_text_2n)-len(tag_sem_con_2n)+1):
                if word_text_2n[k:k+len(tag_sem_con_2n)]==tag_sem_con_2n:
                    bio_labble[k:k+len(tag_sem_con_2n)]=bio_tag
                    found = True
            if found==True:
                tag_list.append(tag_sem_tag)
                text_list.append(tag_sem.iloc[j, 4])
            else:
                notfind_tag_list.append(tag_sem_tag)
                notfind_text_list.append(tag_sem.iloc[j, 4])
                
        save_list=[str(word_df.iloc[i, 0]),"\t",str(word_text_2n),"\t",str(bio_labble),"\t",str(tag_list),"\t",str(text_list),"\t",str(notfind_tag_list),"\t",str(notfind_text_list),"\n"]
        bio_txt.writelines(save_list)
    else: #直接輸出句子以及[00000001]
        shi_labble[7]=1
bio_txt.close()
df = pd.read_csv("bert_code/bert_data/bert/class_02_ch_bio.txt", sep="\t", header=None,)#檢查哪個字沒找到
not_spa=df[df[5]!='[]'] #檢查哪個字沒找到