#!/usr/bin/env python
# coding: utf-8

# In[26]:


import os
import json
local=r"G:\AI_CUP\data_AI_CUP\private_result_AI_CUP\local_EN\\"


# In[27]:


task1=os.listdir(local+"task1")


# In[28]:


ord("三")


# In[29]:


chr(19979)


# In[30]:


x=["零","一","二","三","四","五","六","七","八","九","十"]


# In[42]:


sen=[]
sym=[]
for i in range(26):
    sen.append(chr(97+i))
    sen.append(chr(65+i))
for i in range(10):
    sen.append('{}'.format(i))


# In[43]:


sen=sen+x


# In[44]:


sen


# In[45]:


for j in task1:
    with open(local+"task1\\"+j,"r",encoding="utf-8") as f:
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


# In[46]:


sym


# In[47]:


b=""


# In[48]:


for i in sym:
    b=b+i+"$"


# In[49]:


b


# In[50]:


with open("symbol.txt","w",encoding="utf-8") as f:
    f.write(b)
f.close()


# In[51]:




# In[ ]:




