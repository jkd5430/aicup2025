#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os


# In[4]:


with open("task2_answer.txt","r",encoding="utf-8") as f:
    x=f.read()
f.close()


# In[16]:


b=[]
for i in x.split("\n"):
    if len(i) < 100:
        b.append(i)


# In[65]:


types=["PATIENT", "DOCTOR" ,"USERNAME" ,"FAMILYNAME","PERSONALNAME","ROOM", "DEPARTMENT", "HOSPITAL", "ORGANIZATION", "STREET", "CITY", "DISTRICT", "COUNTY", "STATE", "COUNTRY", "ZIP", "LOCATIONOTHER","DATE", "TIME", "DURATION", "SET","PHONE", "FAX", "EMAIL", "URL", "IPADDRESS","SOCIAL_SECURITY_NUMBER", "MEDICAL_RECORD_NUMBER", "HEALTH_PLAN_NUMBER", "ACCOUNT_NUMBER", "LICENSE_NUMBER", "VEHICLE_ID", "DEVICE_ID", "BIOMETRIC_ID", "ID_NUMBER","PROFESSION","AGE"]


# In[30]:


print(types)


# In[45]:


bx=[]
havet=[]
for i in b:
#     if i.split(" ")[0]=="71995":
#         print(i)
    try:
        i.index("think")
        
        print(i)
    except:
        x=i.replace("-" ,"")
        x=x.replace("[","")
        x=x.replace("]","")
        if '\t' in x:
            havet.append(x)
        else:
            bx.append(x)


# In[87]:


havet
bx=bx[:-1]


# In[92]:


ans=[]
for i in bx:
    count=0
    ds=i.split(" ")
    ds = [item for item in ds if item != ""]
    
#     print(ds)
#     try:
    for j in types:
        if j in ds[1]:
            count=1
    if count==0:
        None
    else:
        ans.append(ds)
        


# In[98]:


full_name = ' '.join(ans[0][2:])


# In[101]:


anss=[]
for i in ans:
    full_name=' '.join(i[2:])
    b=i[:2]
    b.append(full_name)
    anss.append(b)


# In[102]:


# anss


# In[149]:


havett=[]
for i in havet:
    asd=i.split("\t")
    dsd=asd[0].split("  ")
    print(asd)
    if asd[1][-1]!=" ":
        word=asd[1]
    else:
        for s in range(len(asd[1])):
    #         print(asd[1])
            if asd[1][-(s+1)]!=" ":
    #             print(s+1)
                word=asd[1][:-(s)]
#                 print(word)
                break
    print(word)
    havett.append(dsd+[word])


# In[150]:


# havett


# In[153]:


d=anss+havett


# In[156]:


xd=[]
for i in d:
    try:
        xd.index(i)
    except:
        xd.append(i)


# In[162]:


x=""
for i in xd:
    x=x+i[0]+"\t"+i[1]+"\t"+i[2]+"\n"


# In[165]:


with open("clean.txt","w",encoding="utf-8") as f:
    f.write(x)
f.close()

