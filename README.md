# aicup2025
## 創建環境
任務一 whisperX環境
    
    conda env create -f whisperx.yml
任務二 Qwen3以及BERT環境  
    
    conda env create -f qwen3.yml
****
## 任務一 語音轉文字 
使用以下程式碼，啟動whisperx.yml環境

    conda acitvate <your_env_whisperx>
    
使用以下程式碼，將錄音檔轉為文字稿  

    python task1_whisper.py
*請將檔案內 `audio_dir` 更換為所需的錄音檔案
    
使用以下程式碼，將文字稿整合成上傳txt檔案  

    python task1flie_2_task1ans.py
*請將檔案內 `path` 更換為你在task1_whisper.py存放的task1檔案位置

****
## 任務二 命名實體識別任務
使用以下程式碼，啟動qwen3.yml環境  

    conda acitvate <your_env_qwen3>
由於本組中文英文分開處理，故首先將txt以及json檔案的中文與英文分開    
*需修改 `split_ch_en`、`split_json_ch_en` 檔案內 `folder_path` 資料夾路徑  
txt檔案使用

    python split_ch_en.py

json檔案使用  

    python split_json_ch_en.py
    
## 處理英文檔案
使用以下程式碼，對英文文字稿做推論   
    
    python RAG.py
*需修改檔案內 `alocal`、`blocal`改成data_AI_CUP資料夾路徑，157行以及166行需改成split_ch_en.py所建立的en資料夾
    
使用以下程式碼，清理推論結果中不需要的文字  
        
    python clean_data.py
*需修改`clean_data`檔案內的第13行設定由RAG.PY生出的private_result_advance_EN檔案，第168行設定輸出檔案位置
    
使用以下程式碼，找出敏感字詞中的特殊字元       

    python English_find_symbol.py
*需修改`English_find_symbol` 檔案內 `local` 改成split_ch_en.py所建立的en資料夾
    
使用以下程式碼，將文字稿的敏感字詞對回去json檔中的時間以抓出敏感字詞的時間序  
       
    python English_timestep.py
    
*需修改`English_timestep` 檔案內`local` 改成split_ch_en.py以及split_json_ch_en.py所建立的en資料夾  
*第140行為English_find_symbol.py找出的"symbol.txt"    
*第147行為clean_data.py找出的"clean.txt"   
*第289、297行需設定輸出資料夾分別為有對到時間序的檔案及沒對到時間序的檔案
    
使用以下程式碼，將英文檔案中沒有對到的檔案進行模糊查詢再匹配一次  

    python fuzzy.py
    
*需修改 `fuzzy` 檔案內 `p_txt`、`output_txt`、`json_folder`，分別代表英文沒對到的檔案、輸出路徑英文json檔案    
*其中`p_txt`是English_timestep.py生出的"14B_best_match_other.txt"，`json_folder`是split_json_ch_en.py所建立的en資料夾
## 處理中文檔案  
使用以下程式碼，對中文文字稿做推論    
    
    python ch_connect.py
*需修改 `ch_connect.py` 檔案內 `INPUT_FOLDER` 是split_ch_en.py所建立的ch資料夾
使用以下程式碼，清理推論結果中不需要的文字  

    python ch_clean_predictions.py
*需修改`ch_clean_predictions.py`檔案內 `input_path`是由ch_connect.py所設定的OUTPUT_PATH
使用以下程式碼，找出敏感字詞中的特殊字元  
    
    python ch_find_symbol.py
*需修改`ch_find_symbol.py` 檔案內 `local` 是split_ch_en.py所建立的ch資料夾
使用以下程式碼，將文字稿的敏感字詞對回去json檔中的時間以抓出敏感字詞的時間序  
   
    python ch_timestep.py 
*需修改`ch_timestep.py` 檔案內`local`  改成split_ch_en.py以及split_json_ch_en.py所建立的ch資料夾  
*第141行"symbol.txt"為ch_find_symbol.py所生成
*第148行需改成由ch_clean_predictions.py設定的output_path位置
*第252、260行需設定輸出資料夾分別為有對到時間序的檔案及沒對到時間序的檔案
輸出結果及為任務二中文的敏感字詞結果
    
*合併中英文結果
使用以下程式碼，將中文英文檔案合併成最終結果  

    python concate.py
*需修改`concate`檔案內第20行，分別將中英文的timestep的txt合併
##BERT
使用以下程式碼，將官方給的資料集標註成BIO格式
    
    python bio.py 
*需修改`bio.py `檔案內`ann_df`需改成任一task2_answer.txt，`word_df`需改成任一task1_answer.txt，`bio_txt`是bio標註檔案的存放位置    
使用以下程式碼，進行BERT訓練
    
    python bert_train.py
*其中資料均放在bert_code/bert_data/bert/位置裡    
使用以下程式碼，進行BERT預測    
    
    python bert_pred.py
*其中第168行放task1_whisper.py所生成的"result_val_all_number/task2_json"    
*其中第170行設定存放位置







    
