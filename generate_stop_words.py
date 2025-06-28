# generate_stop_words.py
import pandas as pd
import collections
import os
import jieba

ARTICLE_CSV_PATH = "dataset/articles.csv"
STOP_WORDS_OUTPUT = "config/custom_stop_words.txt"
TOP_N = 100

os.makedirs("config", exist_ok=True)

# 讀取文章語料
df = pd.read_csv(ARTICLE_CSV_PATH)
texts = df["content"].astype(str).tolist()
all_text = "\n".join(texts)

# 使用 jieba 做繁中斷詞（可自訂詞典）
tokens = jieba.lcut(all_text)

# 過濾：只留長度 >= 2 的詞、去除符號與數字
tokens = [t for t in tokens if len(t) >= 2 and t.isalpha()]

# 統計詞頻
counter = collections.Counter(tokens)
common_words = counter.most_common(TOP_N)

# 儲存為 txt 檔
with open(STOP_WORDS_OUTPUT, "w", encoding="utf-8") as f:
    for word, freq in common_words:
        f.write(f"{word}\n")

print(f"✅ 已儲存前 {TOP_N} 個高頻詞至 {STOP_WORDS_OUTPUT}")
