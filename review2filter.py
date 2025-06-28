# review2filter.py
import pandas as pd
import os

INPUT_CSV = "dataset/tag_review_llm.csv"
FUSION_CSV = "dataset/suggested_tags_fusion.csv"
OUT_CSV = "dataset/suggested_tags_fusion_llm_filtered.csv"

# 讀取 LLM 評估結果與原始貼標資料
df_review = pd.read_csv(INPUT_CSV)
df_fusion = pd.read_csv(FUSION_CSV)

# 建立過濾對照表
filtered_set = set()
for _, row in df_review.iterrows():
    tag = str(row["tag"]).strip()
    slug = str(row["slug"]).strip()
    if str(row.get("should_filter", False)).lower() in {"true", "yes", "1"}:
        filtered_set.add((slug, tag))

# 過濾處理
rows = []
for _, row in df_fusion.iterrows():
    slug = str(row["slug"]).strip()
    tags = [t.strip() for t in str(row["tags_merged"]).split(",") if t.strip()]
    filtered = [t for t in tags if (slug, t) in filtered_set]
    cleaned = [t for t in tags if (slug, t) not in filtered_set]
    rows.append({
        "slug": slug,
        "title": row["title"],
        "tags_llm_filtered": ", ".join(cleaned),
        "tags_llm_removed": ", ".join(filtered)
    })

df_out = pd.DataFrame(rows)
os.makedirs("dataset", exist_ok=True)
df_out.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ LLM 多維過濾結果已儲存：{OUT_CSV}")
