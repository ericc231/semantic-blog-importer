# filter_tags.py
import pandas as pd
from tag_cleaner import clean_tags
from collections import Counter

INPUT_CSV = "dataset/suggested_tags_fusion.csv"
OUTPUT_CSV = "dataset/suggested_tags_fusion_cleaned.csv"

df = pd.read_csv(INPUT_CSV)
removed_counter = Counter()

for col in ["tags_zh", "tags_keybert", "tags_merged"]:
    df[col] = df[col].fillna("").apply(
        lambda x: ", ".join(clean_tags([t.strip() for t in x.split(",") if t.strip()], removed_counter))
    )

df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ 已清洗完成 → {OUTPUT_CSV}")

print("\n🧹 髒標籤統計（出現 ≥ 2）：")
for tag, count in removed_counter.most_common():
    if count >= 2:
        print(f"  {tag} → {count} 次")
