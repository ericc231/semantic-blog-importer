# generate_suffixes_from_corpus.py
import pandas as pd
from collections import Counter
import os

INPUT_CSV = "dataset/suggested_tags_fusion.csv"
OUTPUT_PATH = "config/suffixes_candidates.csv"
TOP_N = 300

df = pd.read_csv(INPUT_CSV)
tags = []

for col in ["tags_zh", "tags_keybert", "tags_merged"]:
    if col in df.columns:
        for entry in df[col].dropna():
            tags.extend([t.strip() for t in str(entry).split(",") if t.strip()])

suffix_counter = Counter()
for tag in tags:
    if len(tag) <= 6:
        for k in range(2, 4):  # 最多 3 字後綴
            if len(tag) > k:
                suffix = tag[-k:]
                suffix_counter[suffix] += 1

df_out = pd.DataFrame(suffix_counter.most_common(TOP_N), columns=["suffix", "count"])
os.makedirs("config", exist_ok=True)
df_out.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
print(f"✅ 推測的潛在後綴詞已儲存至：{OUTPUT_PATH}")
