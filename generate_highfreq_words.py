# generate_highfreq_words.py
import os
import pandas as pd
import jieba
from collections import Counter

INPUT_CSV = "dataset/articles.csv"
OUTPUT_CSV = "config/highfreq_words.csv"
TOP_N = 500

# 讀取語料
df = pd.read_csv(INPUT_CSV)
texts = df["content"].dropna().astype(str).tolist()
print(f"📄 共讀入 {len(texts)} 篇文章")

# jieba 斷詞並統計詞頻
counter = Counter()
for text in texts:
    words = jieba.lcut(text)
    words = [w.strip() for w in words if len(w.strip()) >= 2]
    counter.update(words)

# 取前 N 高頻詞
most_common = counter.most_common(TOP_N)
df_out = pd.DataFrame(most_common, columns=["word", "count"])
os.makedirs("config", exist_ok=True)
df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ 已儲存前 {TOP_N} 高頻詞至：{OUTPUT_CSV}")
