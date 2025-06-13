import os
import json
from fuzzywuzzy import fuzz, process

p_txt = r"C:\Users\xinyou\OneDrive\桌面\14B_best_match_other.txt"
output_txt = r"C:\Users\xinyou\OneDrive\桌面\matched_clean_output_2.txt"
json_folder = r"C:\Users\xinyou\OneDrive\桌面\task2_json" 
json_cache = {}


with open(p_txt, 'r', encoding='utf-8') as f:
    txt_l = [line.strip() for line in f if line.strip()]

with open(output_txt, 'w', encoding='utf-8') as out_f:
    for line in txt_l:
        parts = line.split()
        if len(parts) >= 3:
            key = parts[0]
            label = parts[1]
            original_value = parts[2]

            json_key = key.split('_')[0]
            json_filename = f"{json_key}.json"
            json_path = os.path.join(json_folder, json_filename)

            if json_key not in json_cache:
                if os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf-8') as jf:
                        data = json.load(jf)
                        words = [w['word'].strip() for seg in data for w in seg.get("words", []) if w['word'].strip()]
                        json_cache[json_key] = list(set(words))
                else:
                    json_cache[json_key] = []

            candidates = json_cache[json_key]
            if candidates:
                match, score = process.extractOne(original_value, candidates, scorer=fuzz.ratio)
            else:
                match = original_value

            cleaned_match = match.replace('""', ' ')
            out_f.write(f"{key}\t{label}\t{cleaned_match}\n")
