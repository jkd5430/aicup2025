import os
import random
import requests
from pathlib import Path
from tqdm import tqdm
import pandas as pd

# === 設定參數 ===
INPUT_FOLDER   = r"G:\AI_CUP\data_AI_CUP\private_result_AI_CUP\task1_CN"  # <-- 改成你的 TXT 資料夾路徑
OUTPUT_PATH    = "./private_result_task2_CN.txt"
LM_STUDIO_URL  = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME     = "qwen3-32b"  # <-- 替換為你的模型名稱

# === Step 1: 讀取所有 .txt 檔案，檔案名當 id，內容當 text ===
all_data = []
for file in Path(INPUT_FOLDER).glob("*.txt"):
    file_id = file.stem  # e.g. "23.txt" -> "23"
    with open(file, "r", encoding="utf-8") as f:
        text = f.read().strip()
    all_data.append({"id": file_id, "text": text})

base_system="""你是一位敏感資訊標註專家。根據以下文字內容，判斷其是否包含任何敏感資訊。你的任務如下：

你必須根據語境判斷可能的敏感詞彙，然後依照標註準則進行驗證。

請根據我提供的「敏感資訊分類」進行偵測與分類。

對於每一個被偵測出的敏感詞，請用以下格式輸出：
[分類] [敏感詞]

每行一筆。

敏感資訊的分類僅限於以下這些：
PATIENT / DOCTOR / USERNAME / FAMILYNAME / PERSONALNAME / PROFESSION / ROOM / DEPARTMENT / HOSPITAL / ORGANIZATION / STREET / CITY / DISTRICT / COUNTY / STATE / COUNTRY / ZIP / LOCATION-OTHER / AGE / DATE / TIME / DURATION / SET / PHONE / FAX / EMAIL / URL / IPADDRESS / SOCIAL_SECURITY_NUMBER / MEDICAL_RECORD_NUMBER / HEALTH_PLAN_NUMBER / ACCOUNT_NUMBER / LICENSE_NUMBER / VEHICLE_ID / DEVICE_ID / BIOMETRIC_ID / ID_NUMBER / OTHER

如果相同的敏感詞在文字中出現多次，即使屬於同一類別，也請每次出現都分別標註。

如果沒有任何敏感詞，請輸出：None。

每一句話都必須逐一比對所有敏感資訊分類定義，並據此進行分類。

以下是每個分類的詳細定義：

[Name]
This is the SHI category that mentions the name of a patient or a doctor or nurse etc. Basically any mention of a
person’s name should be annotated under this category. There are 5 sub-categories-PATIENT, DOCTOR
USERNAME, PERSONALNAME
The following rules should be followed while annotating a name:
1. Annotate the entire name or the initials in the text.
2. Titles (Dr., Mr., Ms., etc.) do not have to be annotated.
3. Information such as "M.D.", "R.N." do not have to be annotated.
4. If a name is possessive (e.g., Sam's) do not annotate the 's
5. USERNAME category be used for SHI that are initials followed by numbers (i.e., as4)
6. All the names of any professor, registrar, nurse etc. should be annotated as Doctor.
7. The initials of the doctors should be annotated.
8. If a nickname can be used to determine the person's real identity, it should be annotated under one of the
applicable categories (PATIENT, DOCTOR USERNAME, FAMILYNAME.).
9.When a phrase contains a possessive structure such as “X's mom” or “X's dad,” consider tagging X as FAMILYNAME if it refers to a person who is a relative of the mentioned family role.
10.If the same name appears multiple times within the same sentence, and at least one occurrence is used in a possessive family structure (e.g., "Ivan's mom"), then all instances of that name in that sentence should be tagged as FAMILYNAME.
11.FAMILYNAME：If the semantic context is set in a hospital, any name that appears without explicitly indicating medical staff should be considered a patient’s family member and annotated as FAMILYNAME.
12.PERSONALNAME：Other names that have no blood relation to the patient.




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
"""



# === Step 3: 串接 LM Studio 並取得回應 ===
headers = {"Content-Type": "application/json"}
results = []

for item in tqdm(all_data, desc="Querying LM Studio"):
    payload = {
        "model": "qwen3-32b",
        "messages": [
            {"role": "system",   "content": base_system},
            {"role": "user",   "content": item["text"]}
        ],
        "temperature": 0,
        "max_tokens": 4900,  
        "top_p": 1.0,           # Nucleus sampling 關閉（因為 temperature=0 已確定是 deterministic）
        "top_k": 0,             # top_k = 0 代表不做 top-k sampling
        "do_sample": False,
        "seed": 42,
        "stream": False
    }
    try:
        resp = requests.post(LM_STUDIO_URL, headers=headers, json=payload, timeout=300)
        resp.raise_for_status()
        answer = resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        answer = f"[ERROR] {e}"

    results.append({
        "id": item["id"],
        "prediction": answer
    })

# === Step 4: 儲存成 TSV（.txt）檔 ===
df = pd.DataFrame(results)
df.to_csv(OUTPUT_PATH, sep="\t", index=False, header=False)

print(f"✅ 完成！共處理 {len(df)} 筆資料，預測結果儲存在：{OUTPUT_PATH}")
