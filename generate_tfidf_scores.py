# generate_tfidf_scores.py
import os
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer

INPUT_CSV = "dataset/articles.csv"
OUTPUT_CSV = "config/tfidf_scores.csv"

df = pd.read_csv(INPUT_CSV)
texts = df["content"].dropna().astype(str).tolist()

def jieba_tokenizer(text):
    return [w.strip() for w in jieba.lcut(text) if len(w.strip()) >= 2]

# TF-IDF 建模
vectorizer = TfidfVectorizer(tokenizer=jieba_tokenizer)
X = vectorizer.fit_transform(texts)
vocab = vectorizer.get_feature_names_out()
scores = X.sum(axis=0).A1  # 每詞總 tf-idf 分數

df_out = pd.DataFrame({"word": vocab, "tfidf": scores})
df_out = df_out.sort_values("tfidf", ascending=False)
os.makedirs("config", exist_ok=True)
df_out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ TF-IDF 分數已寫入 {OUTPUT_CSV}")
