import os
import json
import shutil
import re

# 中文偵測函式
def contains_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

# 設定資料夾路徑
folder_path = r"C:\Users\xinyou\OneDrive\桌面\result\task2_json"

# 建立分類子資料夾
os.makedirs(os.path.join(folder_path, 'zh'), exist_ok=True)
os.makedirs(os.path.join(folder_path, 'en'), exist_ok=True)

# 處理所有 .json 檔案
for filename in os.listdir(folder_path):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(folder_path, filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 只要有一筆 "text" 包含中文，就分類為中文
        is_chinese = any(
            contains_chinese(entry.get("text", "")) for entry in data if isinstance(entry, dict)
        )

        target_folder = 'zh' if is_chinese else 'en'
        shutil.move(file_path, os.path.join(folder_path, target_folder, filename))

    except Exception as e:
        print(f" 無法處理 {filename}：{e}")
