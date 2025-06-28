# semantic_review_log.py
import pandas as pd
from semantic_distance import get_similarity

CSV_PATH = "dataset/suggested_tags_fusion.csv"
LOG_PATH = "tagging_report/semantic_tag_removals.csv"
SIM_THRESHOLD = 0.2

df = pd.read_csv(CSV_PATH)
rows = []

print("🔎 分析每個 tags_merged 相對標題的語意相似度...")

for _, row in df.iterrows():
    slug = row["slug"]
    title = row["title"]
    tags = [t.strip() for t in str(row["tags_merged"]).split(",") if t.strip()]

    for tag in tags:
        sim = round(get_similarity(tag, title), 4)
        keep = sim >= SIM_THRESHOLD
        rows.append({
            "slug": slug,
            "title": title,
            "tag": tag,
            "similarity": sim,
            "keep": keep
        })

pd.DataFrame(rows).to_csv(LOG_PATH, index=False, encoding="utf-8-sig")
print(f"📁 剃除審計記錄已輸出：{LOG_PATH}")
