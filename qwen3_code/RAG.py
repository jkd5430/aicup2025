#!/usr/bin/env python
# coding: utf-8

# In[1]:

from tqdm import tqdm
import os
import json
import random
random.seed(42)
alocal=r"E:\data_AI_CUP\training_Data1_label\\" #traindata1_task1_task2_label
blocal=r"E:\data_AI_CUP\training_Data2_label\\" #traindata2_task1_task2_label

# In[2]:


def dopen(alocal,file_name):
    with open(alocal+file_name,"r",encoding="utf-8") as f:
        x=f.read()
    f.close()
    x=x.split("\n")
    if x[-1]=="":
        x.pop(-1)
    return x


# In[3]:


def senword_to(text2,output):
    bbd1=""
    i=text2[output['ids'][0][0]]['word']
    bbd1+="text:"+i+"\nsensetive:\n"
    for i,j in text2[output['ids'][0][0]]['sensitive']:
        bbd1+="{}\t{} \n".format(i,j)
    return bbd1


# In[4]:


def make_data(alocal):
    task1=dopen(alocal,"task1_answer.txt")
    task2=dopen(alocal,"task2_answer.txt")
    # 初始化空字典和 id 列表
    text = {}
    idss = []
    
    # 1) 处理 task2，累积 sensitive 列表
    for line in task2:
        parts = line.split("\t")
        if len(parts) < 5:
            # 跳過格式不對的行，但繼續處理下一行
            print("跳過 malformed line:", repr(line))
            continue
        try:
            _id, _type, word = parts[0], parts[1], parts[4]
            # 如果 _id 不存在，就插入 {'sensitive': []}
            text.setdefault(_id, {'sensitive': []})
            text[_id]['sensitive'].append([_type, word])
        except:
            # print(line)
            break
    # 2) 处理 task1，插入 word 字段，同时保留已有的 sensitive
    for line in task1:
        parts = line.split("\t")
        ids, word = parts[0], parts[1]
        idss.append(ids)
    
        # 把双引号换成单引号
        word = word.replace('"', "'")
    
        # 如果之前没出现过，就先创建一个带 sensitive 空列表的 entry
        text.setdefault(ids, {'sensitive': []})
        text[ids]['word'] = word
    
    # （可选）去重 idss
    idss = list(dict.fromkeys(idss))
    return text,idss


# In[5]:


text,idss=make_data(alocal)
text2,idss2=make_data(blocal)


# In[6]:


import chromadb

class chroma():
    def __init__(self,word,toto,ids,word2,toto2,ids2):
        chroma_client = chromadb.Client()
        
        self.collection = chroma_client.create_collection(name="my_collection")
        self.collection2 = chroma_client.create_collection(name="my_collection2")
        self.collection.add(
            documents=word,
            metadatas=toto,
            ids=ids
        )
        self.collection2.add(
            documents=word2,
            metadatas=toto2,
            ids=ids2
        )
    def check(self,query,n_results=1):
        results=self.collection.query(
        query_texts=[query],
        n_results=n_results
        )
        results2=self.collection2.query(
        query_texts=[query],
        n_results=n_results
        )
        return results,results2


# In[7]:


def chroma_data(text,idss):
    toto=[]
    word=[]
    num=0
    for i in idss:
        word.append(text[i]['word'])
        if text[i]['sensitive']==[]:
            toto.append({'source': 'doc{}{}'.format("0",num)})
        else:
            toto.append({'source': 'doc{}{}'.format("1",num)})
    return toto,word


# In[8]:


toto1,word1=chroma_data(text,idss)
toto2,word2=chroma_data(text2,idss2)


# In[9]:


y=chroma(word1,toto1,idss,word2,toto2,idss2)


# # this is test

# In[10]:


def test_data(x1):
    with open(r"E:\AI_CUP\code_AI_CUP\AI_CUP_task1_code\private_result_AI_CUP\task1\{}".format(x1),"r",encoding="utf-8") as f:
        x=f.read()
    f.close()
    return x


# In[11]:


idsd=os.listdir(r"E:\AI_CUP\code_AI_CUP\AI_CUP_task1_code\private_result_AI_CUP\task1")


# In[13]:


import requests
url = "http://127.0.0.1:1234/v1/chat/completions"
headers = {
    "Content-Type": "application/json"
}


# In[ ]:


base_system="""You are a sensitive information annotation expert. Based on the following text content, determine whether it contains any sensitive information. You are required to:

You must first determine the sensitive terms based on the context, and then verify them using the annotation guidelines.

Detect and classify based on the "sensitive information categories" I provide.

For each sensitive term found, output it in the format:
"[CATEGORY] [SENSITIVE_TERM]", one line per term.

Sensitive categories are limited to the following:
PATIENT / DOCTOR / USERNAME / FAMILYNAME / PERSONALNAME / PROFESSION / ROOM / DEPARTMENT / HOSPITAL / ORGANIZATION / STREET / CITY / DISTRICT / COUNTY / STATE / COUNTRY / ZIP / LOCATION-OTHER / AGE / DATE / TIME / DURATION / SET / PHONE / FAX / EMAIL / URL / IPADDRESS / SOCIAL_SECURITY_NUMBER / MEDICAL_RECORD_NUMBER / HEALTH_PLAN_NUMBER / ACCOUNT_NUMBER / LICENSE_NUMBER / VEHICLE_ID / DEVICE_ID / BIOMETRIC_ID / ID_NUMBER / OTHER

If the same sensitive term appears multiple times in the text, even if under the same category, please annotate each occurrence separately.

If there are no sensitive terms, please output None.

Each sentence must be reviewed against all category definitions and classified accordingly.

The following are the detailed definitions of each category：

[Name]
This is the SHI category that mentions the name of a patient or a doctor or nurse etc. Basically any mention of a
person’s name should be annotated under this category. There are 5 sub-categories-PATIENT, DOCTOR
USERNAME, PERSONALNAME
The following rules should be followed while annotating a name:
1.All texts in this project are medical records. Unless explicitly identified as “medical staff,” “hospital personnel,” or “family member,” any personal name shall by default be assumed to refer to the patient and classified as PATIENT.
2. Annotate the entire name or the initials in the text.
3. Titles (Dr., Mr., Ms., etc.) do not have to be annotated.
4. Information such as "M.D.", "R.N." do not have to be annotated.
5. If a name is possessive (e.g., Sam's) do not annotate the 's
6. USERNAME category be used for SHI that are initials followed by numbers (i.e., as4)
7. All the names of any professor, registrar, nurse etc. should be annotated as Doctor.
8. The initials of the doctors should be annotated.
9. If a nickname can be used to determine the person's real identity, it should be annotated under one of the
applicable categories (PATIENT, DOCTOR USERNAME, FAMILYNAME.).
10.When a phrase contains a possessive structure such as “X's mom” or “X's dad,” consider tagging X as FAMILYNAME if it refers to a person who is a relative of the mentioned family role.
11.If the same name appears multiple times within the same sentence, and at least one occurrence is used in a possessive family structure (e.g., "Ivan's mom"), then all instances of that name in that sentence should be tagged as FAMILYNAME.
12.All texts in this project are medical records. Unless explicitly identified as “medical staff,” “hospital personnel,” or “family member,” any personal name shall by default be assumed to refer to the patient and classified as PATIENT.
13.PERSONALNAME: Used for names of third parties who are not the patient, not the patient’s relatives, and not medical personnel, such as insurance agents, social workers, drivers, or police officers.
14.If the person's role cannot be clearly determined and there is no possessive structure indicating a family relationship, follow the prior guideline: default to assuming the person is the patient → label as PATIENT.




[Location]
This SHI is the mention of any physical location. It may be the hospital name, the department in a hospital, the name
of an organization, address of the patient, city, country etc. It has multiple sub-categories including the parts of an
address or an organization, hospital, department etc. The rules for annotating a location are as follows:
1. Annotate state/country names as well as addresses and cities.Each part of an address willgetits
owntag.
2. Generic locations (i.e., "hair salon", “golf course”, “retail store”) need to be annotated along with
named organizations (i.e., "UNSW").
3. If there’s a name of a medical facility and you’re not sure if it should be a HOSPITAL or a DEPARTMENT,
you should probably go with HOSPITAL.
4. “POW C” should be tagged as HOSPITAL(POW) ROOM(C)
5. Hospital room numbers should be annotated as ROOM
6. Floors and suites can also be annotated as ROOM
7. “Floor 2, room 2” can all be one ROOM tag
8. Annotate state/country names as well as addresses and cities. Each part of an address will get its own tag.
9. The departments inside of hospitals should be annotated, but only if they are unique. There is a list of generic
hospital units at the end of this file; if a department is not on that list, it should be annotated.
10. Medical facilities should not be marked as organizations.
11. All the components of an address should be marked including the street, district, city, state, zip. For example if
the address is mentioned as :
1 TODMAN AVENUE
FARMBOROUGH HEIGHTS NSW 2526
Annotate the following:
‘1 TODMAN AVENUE’-Street
‘FARMBOROUGH HEIGHTS’-City
‘NSW’- State
‘2526’-Zip
12. LOCATION-OTHER: Used for locations that cannot be categorized as Street/City/District/County/State/Country/Zip/Hospital/Department/Organization/Room, such as “Andover” (small town), “Canterbury” (historical/religious town),“Golden Gate Bridge” (landmark), or “Chicago metro area” (metropolitan area), which are composite landmarks.
13.Only annotate organizations that are large in scale and related to medical services or health records; do not annotate small general businesses.
14.If a place name refers to an administrative district or county of a large city (e.g., Greenwich), annotate it as DISTRICT.

[Age]
Any mention of age should be annotated. The annotator should annotate the number for age and not the associated
text. Annotators should annotate all ages, not just those over 90, including those for patient's families if they are
mentioned.
Expressions like “20s” (or “30s,” “40s,” etc.), which denote “in their twenties,” should also be annotated as AGE.

[Date]
In this project, any kind of temporal expression within the text should be annotated. Temporal expressions are
phrases that contain time information. The types of temporal expressions that we need to mark include date
(represented by the subcategory DATE), time (represented by the subcategory TIME), duration (represented
by the subcategory DURATION) and frequency (represented by the subcategory SET). Dates are an
important SHI because the dates include date of births which can be used to get the age of the patient. Dates
can take a varieties of formats, like, ‘/’ or ‘-‘ as the separator, just the date and month, only the year, the
month as a number or in words etc. Thus, the annotators need to identify any format of temporal expressions and
annotate by using one of the subcategory tags. The detailed guidelines to annotate the temporal expressions are as
follows:
1. Any calendar date, including years, seasons, months, holidays, time of day, and specific weeks
(e.g., Week 10, last week,today,now), should be annotated.Days of the week should also be annotated
2. If the phrase has 's (i.e., "in the '90s'), annotate "'90s"
3. Include annotations of seasons ("Fall '02")
4. Include quote marks that stand in for years ("'92")
5.Even if a temporal phrase does not contain numbers , still annotate it as DATE if it clearly refers to a specific calendar date.
6.Detect and annotate any frequency expressions (e.g., "daily", "weekly", "monthly", "annually", "hourly", "periodically") as SET.
e.g.
SET every day/couple of times
DATE today
DATE Last week
TIME Last night
TIME that night
TIME morning / afternoon
DURATION two weeks
DURATION a couple of hours


[Identifiers] (ID)
Identifiers are numeric or alphanumeric identifiers in the text that would help in the identification of the patient.
These identifiers can be hospital numbers, record numbers, etc. The guidelines to annotate the ids and the examples
of each category are as follows:
1. Any kind of numeric or alphanumeric identifier should be annotated.
2. Only the ID with the hospital name should be annotated as MEDICAL RECORD.
3. Block numbers on which procedures are carried out should be annotated as ID_NUMBER.
4. Lab IDs and Episode Numbers should be annotated as ID_NUMBER.
5. When in doubt, call something a ID_NUMBER
6. Doctor or nurse IDs should be annotated as “other id”
7. No need to label names of devices (for example: “25 mm Carpentier-Edwards magna valve”, “3.5 mm
by 32 mm Taxus drug-eluting stent”, Angioseal”)

[Contact]
This PHI is the data that specifies the details that may help to contact the patient. The examples of this include the
phone number, email, fax etc. Thus, the annotator should annotate any data in the text record that specifies a contact
number for the patient. The following guidelines should be followed:
1. Annotate all the phone numbers, fax numbers, e-mail, URL, IP address, etc.
2. Pager numbers should be annotated as phone numbers.
3. The phone numbers are usually 4 or 8 digit and have the format "02-xxxx-xxxx". It often starts with
"029385" because that's the telephone code for the hospitals to which the records belong.
4. Do not annotate numbers starting with #. They need to follow the format defined below.

[Profession]
The job or the profession of any patient should be annotated under this category. The annotators should annotate any
profession mentioned in the text like carpenter, teacher, lawyer etc. The only exception is the medical profession.
The medical profession related jobs should not be annotated.
1. Any job mentioned for the patient should be annotated.
2. any job that is mentioned that is not held by someone on the medical staff should be tagged
3. College majors are considered professions
4.Any term indicating an occupation or title should be annotated, including religious titles (e.g., Archbishop).

[Other]
Any data that would potentially help in identifying a patient but is not included in the categories above should be
marked as other. The examples of this category include the finger prints, or a company logo etc. The PHI may be an
image rather than just the text.

[Additional]
The section above explains 8 categories and the associated sub-categories along with the examples for each. The
next section mentions some of the general guidelines and tips that would help an annotator in the task:
1. Multiple occurrences of the same PHI should be annotated. If the same PHI exists multiple times within a record then all the instances should be annotated. There are several PHIs that may exists multiple times
like,name, city, hospitals, identifiers etc. For example,Receptors (Block B1): ....
Her-2 in-situ hybridisation: (Her-2 CISH Invitrogen SPOT-Light assay, block B1)
2. Only annotate the information that would need to be replaced when the file is re-identified.
3. When in doubt, annotate!
4. When tagging something that is SHI but it’s not obvious what to tag it as, think about what it should be
replaced by, and whether that will make sense in the document
5. The table below lists words that are generally considered non-markable. However, exceptions apply when
they are necessary to maintain semantic completeness.
For example, while "before" in "before you go" is non-markable, phrases like "in the future", "in the past",
and "all throughout the day" should be annotated as they contribute to the full temporal meaning. This
distinction ensures that only expressions with explicit temporal significance are marked appropriately.
6. The word “now" should be annotated when used in a temporal sense.
Examples:
We need to act now. → Here, now should be annotated as it emphasizes the present moment. DATE now
Now, don’t look at me. I already informed the manager about the issue. → Here, now is used for emphasis
rather than indicating time, so it should not be annotated.
7. The word "time" should be annotated when it refers to time. It should not be annotated when "time" refers
to a situation, occasion, or frequency.
Not annotated: When "time" refers to a situation, occasion, or number of occurrences :
• Each side is hoping this time it will make a difference.
• At the same time
Annotated: When "time" explicitly refers to time :
• You felt calm within a very short time. → DURATION

Please refer to the following examples:
"""


# In[ ]:


outputs=""
for i in tqdm(idsd, desc="Querying LM Studio"):
    query=test_data(i)
    output = y.check(query, n_results=1)
    se1=senword_to(text,output[0])
    se2=senword_to(text2,output[1])
    print(f"Example 1：\n",se1)
    print(f"Example 2：\n",se2)
    dynamic_system = (
        base_system
        + "\nExample 1:\n" + se1
        + "\nExample 2:\n" + se2
        + "\nPlease return only the annotation results in the specified format, without including any examples or additional explanations.\n"
        + "\n\nNow annotate the following text:\n"
    )

    payload = {
        "model": "qwen3-14b",
        "messages": [
            {"role": "system",   "content": dynamic_system},
            {"role": "user",   "content": query}
        ],
        "temperature": 0,
        "max_tokens": 4900,  
        "top_p": 1.0,           # Nucleus sampling 關閉（因為 temperature=0 已確定是 deterministic）
        "top_k": 0,             # top_k = 0 代表不做 top-k sampling
        "do_sample": False,
        "seed": 42,
        "stream": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # 如果返回非 200，会抛出异常
    
    data = response.json()
    # 完整的 响应对象
    # print(data)
    
    # 如果你只想看模型回答的内容：
    content = data["choices"][0]["message"]["content"]
    parts = content.split("</think>")
    thinking = parts[0].strip()                   # 一定存在
    answer   = parts[1].strip() if len(parts) > 1 else ""   # 若沒有第二段就給空字串 
    #如果想看thinking 就print(content[0])

    print("Model says:", thinking)
    print("Answer:", answer)
    for j in answer.split("\n"):
        if j!="":
            outputs+=i[:-4]+"  "+j+"\n"

        with open("private_result_advance_EN_think.txt", "a", encoding="utf-8") as f:
            f.write(thinking)
            f.write("\n")
            f.write(answer)
            f.write("\n")
        f.close()


# # In[ ]:

with open("private_result_advance_EN", "a", encoding="utf-8") as fo:
    fo.write(outputs)
fo.close()


# breakpoint()

# In[ ]:




