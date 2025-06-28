# generate_pos_dict.py
import os
import pandas as pd
import jieba.posseg as pseg
import json

INPUT_CSV = "dataset/articles.csv"
OUTPUT_JSON = "config/pos_dict.json"

df = pd.read_csv(INPUT_CSV)
texts = df["content"].dropna().astype(str).tolist()

word_pos = {}

for text in texts:
    words = pseg.cut(text)
    for w, flag in words:
        if len(w.strip()) >= 2:
            word_pos[w] = flag  # 最後出現為主，或使用 list 並選最多次者

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(word_pos, f, ensure_ascii=False, indent=2)

print(f"✅ 詞性標註已寫入 {OUTPUT_JSON}，共 {len(word_pos)} 詞")
