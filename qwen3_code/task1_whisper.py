import os
import json
from tqdm import tqdm
import whisperx
import gc

device = "cuda"
audio_dir = r"D:\ai_cup\chinese_test_whisperx\data"
name = [f for f in os.listdir(audio_dir) if f.endswith(".wav") or f.endswith(".mp3")]
batch_size = 32
compute_type = "float32"
asr_options = {"suppress_numerals": False}

model = whisperx.load_model("large-v3", device, compute_type=compute_type, asr_options=asr_options)

os.makedirs("result_val_all_number/task2_json", exist_ok=True)
os.makedirs("result_val_all_number/task1", exist_ok=True)


for i in tqdm(name, desc="Transcribing files"):
    audio_path = os.path.join(audio_dir, i)
    audio = whisperx.load_audio(audio_path)


    result = model.transcribe(audio, batch_size=batch_size)


    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)


    merged_text = ''.join(segment['text'] for segment in result["segments"])
    with open(f'result_val_all_number/task1/{i[:-4]}.txt', 'w', encoding="utf-8") as f:
        f.write(merged_text)


    with open(f'result_val_all_number/task2_json/{i[:-4]}.json', 'w', encoding='utf-8') as f:
        json.dump(result["segments"], f, ensure_ascii=False)

