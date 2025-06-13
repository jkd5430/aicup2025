import os
import shutil
import re

# 判斷是否含有中文字元
def contains_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

folder_path = r"C:\Users\xinyou\OneDrive\桌面\result\task1"

# 建立分類資料夾
os.makedirs(os.path.join(folder_path, 'zh'), exist_ok=True)
os.makedirs(os.path.join(folder_path, 'en'), exist_ok=True)

# 遍歷所有 .txt 檔案
for filename in os.listdir(folder_path):
    if not filename.endswith('.txt'):
        continue

    file_path = os.path.join(folder_path, filename)

    # 嘗試讀取檔案內容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 根據是否包含中文分類
        if contains_chinese(content):
            shutil.move(file_path, os.path.join(folder_path, 'zh', filename))
        else:
            shutil.move(file_path, os.path.join(folder_path, 'en', filename))

    except Exception as e:
        print(f"無法處理 {filename}：{e}")
