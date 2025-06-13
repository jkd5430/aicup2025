#!/usr/bin/env python
# coding: utf-8

# In[91]:


import os
import json
local=r"G:\AI_CUP\data_AI_CUP\private_result_AI_CUP\task1_CN"


# In[123]:


# task1=os.path.join(local,"task1")


# In[124]:


ord("三")


# In[125]:


chr(19979)


# In[126]:


x=["零","一","二","三","四","五","六","七","八","九","十"]


# In[127]:


sen=[]
sym=[]
for i in range(26):
    sen.append(chr(97+i))
    sen.append(chr(65+i))


# In[128]:


sen=sen+x


# In[129]:


# In[130]:

print(local)
for j in os.listdir(local):
    file_path = os.path.join(local, j)
    with open(file_path,"r",encoding="utf-8") as f:
        word=f.read()
    f.close()
    # print(word)
    for i in word:
        try:
            sen.index(i)
        except:
            sym.append(i)
        sym=list(set(sym))
        if i=="é":
            print(word,j)
sym.remove(" ")


# In[131]:

print(sym)

# In[132]:


b=""


# In[133]:


# for i in sym:
#     b=b+i+"$"


# In[134]:


# b


# In[135]:


with open("symbol.txt","w",encoding="utf-8") as f:
    f.write(b)
f.close()