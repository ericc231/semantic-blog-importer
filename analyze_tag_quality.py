# analyze_tag_quality.py
import pandas as pd
from semantic_distance import get_similarity
from tag_cleaner import is_noisy, suffix_remover

INPUT_CSV = "dataset/suggested_tags_fusion.csv"
OUTPUT_CSV = "tagging_report/tag_quality_analysis.csv"

df = pd.read_csv(INPUT_CSV)
rows = []

for _, row in df.iterrows():
    slug = row["slug"]
    title = str(row["title"])
    tags = [t.strip() for t in str(row["tags_merged"]).split(",") if t.strip()]

    for tag in tags:
        clean_tag = suffix_remover(tag)
        sim = round(get_similarity(clean_tag, title), 4)
        noisy = is_noisy(clean_tag, title=title)

        reason = []
        if clean_tag != tag:
            reason.append("SuffixRemoved")
        if sim < 0.2:
            reason.append("LowSimilarity")
        if noisy:
            reason.append("Filtered")
        if not reason:
            reason.append("Valid")

        rows.append({
            "slug": slug,
            "title": title,
            "tag": tag,
            "normalized": clean_tag,
            "similarity": sim,
            "status": reason[0]  # 第一個為主因
        })

pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ 標籤品質分析已輸出：{OUTPUT_CSV}")
