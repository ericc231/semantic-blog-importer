# extract_tags_fusion.py
import os
import pandas as pd
import argparse
from collections import Counter
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from model_zh_embed import extract_zh_keywords
from tag_cleaner import clean_tags

ARTICLE_CSV = "dataset/articles.csv"
OUTPUT_CSV = "dataset/suggested_tags_fusion.csv"
STOP_WORDS_PATH = "config/custom_stop_words.txt"
TOP_N = 5
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="union", choices=["union", "vote"])
args = parser.parse_args()

kw_model = KeyBERT(SentenceTransformer(MODEL_NAME))
stop_words = []
if os.path.exists(STOP_WORDS_PATH):
    with open(STOP_WORDS_PATH, "r", encoding="utf-8") as f:
        stop_words = [line.strip() for line in f if line.strip()]

df = pd.read_csv(ARTICLE_CSV)
removed_counter = Counter()
rows = []

for _, row in df.iterrows():
    slug = row["slug"]
    title = row["title"]
    content = str(row["content"])[:2000]

    zh_keywords = extract_zh_keywords(content, top_n=TOP_N)
    tags_zh = [kw for kw, _ in zh_keywords]
    tags_zh = clean_tags(tags_zh, title=title, removed_counter=removed_counter)

    kb_keywords = kw_model.extract_keywords(content, top_n=TOP_N, stop_words=stop_words)
    tags_kb = [kw for kw, _ in kb_keywords]
    tags_kb = clean_tags(tags_kb, title=title, removed_counter=removed_counter)

    if args.mode == "union":
        merged = sorted(set(tags_zh + tags_kb))
    else:
        merged = sorted(set(tags_zh) & set(tags_kb))

    merged = clean_tags(merged, title=title, removed_counter=removed_counter)

    rows.append({
        "slug": slug,
        "title": title,
        "tags_zh": ", ".join(tags_zh),
        "tags_keybert": ", ".join(tags_kb),
        "tags_merged": ", ".join(merged),
    })

pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ 輸出完成 → {OUTPUT_CSV}")

print("\n🧹 髒標籤統計（出現 ≥ 2）：")
for tag, count in removed_counter.most_common():
    if count >= 2:
        print(f"  {tag} → {count} 次")
