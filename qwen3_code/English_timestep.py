#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json


# In[2]:


def opend(local):
    with open(local,"r",encoding="utf-8") as f:
        word=f.read()
    f.close()
    return word
def openj(local):
    with open(local,"r",encoding="utf-8") as f:
        js=json.load(f)
    f.close()
    return js
def normalize(word,sym):
    for i in sym:
        word=word.replace(i,"")
    return word


# In[3]:


def get_data(idss,wod,types,sym):
    if len(idss)==len(wod):
        maps={}
        maps['wod']={}
        maps['type']={}
        for i in range(len(idss)):
            try:
                maps['wod'][idss[i]].append(normalize(wod[i],sym))
                maps['type'][idss[i]].append(types[i])
            except:
                maps['wod'][idss[i]]=[normalize(wod[i],sym)]
                maps['type'][idss[i]]=[types[i]]
        return maps
    else:
        return "wrong"


# In[4]:


def check_list(bl,first,final):
    recd1=0
    recd2=0
    for i2 in bl:
       if i2>=first and recd1==0:
           recd1=i2
       if i2>=final:
           recd2=i2
           break
    return recd1,recd2


# In[5]:


def find_local(bw,bl,recd1,recd2,key):
    recod3=[]
    recod4=[]
    be1=bl.index(recd1)
    fe1=bl.index(recd2)
    key1=key
    check=0
    for j in range((fe1-be1)+1):
        recod5=""
        roundd=be1+j
        
        for i in key1:
            recod5+=i
            try:
                bw[roundd].index(recod5)
            except:
                # print(recod5[:-1])      
                recod5=recod5[:-1]
                recod3.append(recod5)
                recod4.append(roundd)
                bw[roundd]=bw[roundd][:bw[roundd].index(recod5)]+bw[roundd][(len(recod5)+bw[roundd].index(recod5)):]
                check=1
                break
        if check==0:
                # print(recod5,key1)
                recod3.append(recod5)
                recod4.append(roundd)
                bw[roundd]=bw[roundd][:bw[roundd].index(recod5)]+bw[roundd][(len(recod5)+bw[roundd].index(recod5)):]
                break
        else:
            check=0
        # print(recod5)
        key1=key1[len(recod5):]
    return recod3,recod4,bw


# In[17]:


def get_time(recod3,recod4,jstime,jsdit):
    start_time=0
    end_time=0
    for i,j in zip(recod3,recod4):
        x=i.split(" ")
        if len(x)>1:
            for z in x:
                ltime=jstime[j][(jsdit[j].index(z))]
                jsdit[j].remove(z)
                jstime[j].remove(ltime)
                # print(jstime[j][(jsdit[j].index(z))],z)
                if start_time==0:
                    start_time=ltime[0]
        else:
            # print(j,i)
            ltime=jstime[j][(jsdit[j].index(i))]
            jsdit[j].remove(i)
            jstime[j].remove(ltime)
            # print(jstime[j][(jsdit[j].index(i))],i)
            if start_time==0:
                    start_time=ltime[0]
    end_time=ltime[1]
    # print(jsdit)
    return start_time,end_time


# In[18]:


local=r"G:\AI_CUP\data_AI_CUP\private_result_AI_CUP\local_EN\\"
pre=""
task1=os.listdir(local+"task1")
task2_json=os.listdir(local+"task2_json")
sym=opend(r"symbol.txt")
sym=sym.split("$")[:-1]


# In[19]:


with open(r"G:\AI_CUP\code_AI_CUP\AI_CUP_task1_code\matched_clean_output_2.txt","r",encoding="utf-8") as f:
    x=f.read()
f.close()


# In[20]:


for i in range(len(task1)):
    if task1[i][:-4]!=task2_json[i][:-5]:
        print(task1[i][:-4])


# In[21]:


# types=[]
# idss=[]
# wod=[]
# for i in x.split("\n"):
#     asd = i.split(" ")[2].split("\t")
#     if asd[0] != "None":
#         for j in range(5):
#             if i[-(j+1)] != " " and j!=0:
#                 sb=i[:-(j)]
#                 # print("this is:"+sb,i)
#                 break
#             elif i[-(j+1)] != " " and j==0:
#                 sb=i
#                 # print("no change",sb)
#                 break
#         types.append(asd[0].replace("[","").replace("]",""))
#         idss.append(i.split(" ")[0])
#         log=(sb.split(asd[0])[1]).split("\t")
#         if len(log)==1:
#             if log[0][0]==" ":
#                 log=log[0][1:]
#             else:
#                 log=log[0]
#         else:
#             if log[1][0]==" ":
#                 log=log[1][1:]
#             else:
#                 log=log[1]
#         wod.append(log)


# In[22]:


idss=[]
wod=[]
types=[]
for i in x.split("\n"):
    try:
        d=i.split("\t")
        types.append(d[1])
        idss.append(d[0])
        wod.append(normalize(d[2],sym))
    except:
        print(i)
        print("end")

dit=get_data(idss,wod,types,sym)
li=list(set(idss))


# In[23]:


len(wod)


# In[141]:


asdd=""
eother=""
count=0
for ii in li:
    word=opend(local+"task1\\"+ii+".txt")
    jsond=openj(local+"task2_json\\"+ii+".json")
    word=normalize(word,sym)
    jsdit={}
    jstime={}
    for i in range(len(jsond)):
        for j in jsond[i]['words']:
            try:
                jstime[i].append([j['start'],j['end']])
                jsdit[i].append(normalize(j['word'],sym))           
            except:
                try:
                    jstime[i]=[[j['start'],j['end']]]
                    jsdit[i]=[normalize(j['word'],sym)]
                except:
                    None
    # print(jsdit)
    bw=[]
    bl=[]
    for i in jsond:
        aw=normalize(i['text'],sym)
        bw.append(aw)
        if bl != []:
            bl.append(len(aw)+bl[-1])
        else:
            bl.append(len(aw))

    for j,i in zip(dit['type'][ii],dit['wod'][ii]):
        count+=1
        word1=word.lower()
        i=i.lower()
        try:
            try:
                first=word1.index(i)+1
                # i=i+"s" 
            except:
                first=word1.index(i)+1
            final=first+len(i)-1
            
            # print(first,final)
            recd1,recd2=check_list(bl,first,final)
            recd3,recd4,bw=find_local(bw,bl,recd1,recd2,word[first-1:final])
            start_time,end_time=get_time(recd3,recd4,jstime,jsdit)
            # word=word[:first]+word[final:]
            # print("ok")
            sdeda=(final+1-first)*" "
            # print(len(word))
            word=word[:first-1]+sdeda+word[final:]
            # print(len(word))
            # print(ii,i,j,start_time,end_time)      #敏感詞
            asdd=asdd+ii+"\t"+j+"\t"+str(start_time)+"\t"+str(end_time)+"\t"+i+"\n"
        except:
            # print("yes")
            # asdd=asdd+"\nid:"+ii+"\nword:"+word+"\nsensetive:"+i
            eother=eother+ii+"\t"+j+"\t"+i+"\n"
            # print("id:"+ii,"\nword:"+word,"\nsensetive:"+i)     #非敏感詞
            None


# In[138]:


with open(r"14B_best_match.txt","w",encoding="utf-8") as f:
    f.write(asdd)
f.close()


# In[143]:


with open(r"14B_best_match_other.txt","w",encoding="utf-8") as f:
    f.write(eother)
f.close()


# In[140]:


# get_ipython().system('jupyter nbconvert --to script timestep.ipynb')


# In[ ]:




