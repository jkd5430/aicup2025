import pandas as pd
import os 
path=r"G:\AI_CUP\data_AI_CUP\Training_Dataset_02\result_val_all_number\task1"
a=os.listdir(path)
save_path = os.path.join(path, "task1_answer.txt")
save_txt=open(save_path, "w", encoding="utf-8")
for i in a:
    file_path = os.path.join(path, i)
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    save_list=[str(i[:-4]),"\t",str(text),"\n"]
    save_txt.writelines(save_list)
save_txt.close()
