def merge_txt_files(file1_path, file2_path, output_path):
    # 讀取第一個檔案內容
    with open(file1_path, 'r', encoding='utf-8') as f1:
        content1 = f1.read()
    
    # 讀取第二個檔案內容
    with open(file2_path, 'r', encoding='utf-8') as f2:
        content2 = f2.read()
    
    # 合併內容
    merged_content = content1 + content2

    # 寫入新的檔案
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write(merged_content)

    print(f"合併完成，輸出檔案位於：{output_path}")

# 範例用法
merge_txt_files("123.txt", "345.txt", "merged_output.txt")
