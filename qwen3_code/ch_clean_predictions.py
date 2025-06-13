import re

input_path  = "private_result_task2_CN.txt"
output_path = "clean_private_result_task2_CN.txt"

valid_labels = {
    "PATIENT","DOCTOR","USERNAME","FAMILYNAME","PERSONALNAME","PROFESSION","ROOM",
    "DEPARTMENT","HOSPITAL","ORGANIZATION","STREET","CITY","DISTRICT","COUNTY",
    "STATE","COUNTRY","ZIP","LOCATION-OTHER","AGE","DATE","TIME","DURATION","SET",
    "PHONE","FAX","EMAIL","URL","IPADDRESS","SOCIAL_SECURITY_NUMBER",
    "MEDICAL_RECORD_NUMBER","HEALTH_PLAN_NUMBER","ACCOUNT_NUMBER","LICENSE_NUMBER",
    "VEHICLE_ID","DEVICE_ID","BIOMETRIC_ID","ID_NUMBER","OTHER"
}

# 1. 讀整份檔案並以每筆記錄開頭分割
with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()
records = re.split(r'(?m)^(?=\d+\t")', text)

output = []
for rec in records:
    rec = rec.strip()
    if not rec:
        continue

    # 2. 抽出檔案 ID 與整段文字
    m = re.match(r'(\d+)\t["]?(.+)', rec, flags=re.DOTALL)
    if not m:
        continue
    file_id, block = m.group(1), m.group(2)

    # 3. 去掉末尾的 "（如果有）
    if block.endswith('"'):
        block = block[:-1]

    # 4. 移除 <think>…</think>
    block = re.sub(r'<think>.*?</think>', '', block, flags=re.DOTALL).strip()
    if not block:
        continue

    # 5. 逐行檢查，每行同時支援 [LABEL] 和 LABEL
    for line in block.splitlines():
        line = line.strip()
        # 允許前後可有方括號，並且 LABEL 必須在 valid_labels 內
        m2 = re.match(
            rf'^\[?({"|".join(valid_labels)})\]?\s+(.+)$',
            line,
            flags=re.IGNORECASE
        )
        if m2:
            label = m2.group(1).upper()
            word  = m2.group(2).strip()
            output.append(f"{file_id}\t{label}\t{word}")

# 6. 寫出結果
with open(output_path, "w", encoding="utf-8") as fo:
    fo.write("\n".join(output))

print(f"✅ 完成，共擷取到 {len(output)} 筆敏感標註，已寫入 {output_path}")
