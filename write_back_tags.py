# write_back_tags.py
import os
import pandas as pd
import frontmatter

MD_DIR = "exported_md"

CANDIDATES = [
    ("🤖 LLM清洗後貼標", "dataset/suggested_tags_fusion_llm_filtered.csv"),
    ("📄 原始貼標融合", "dataset/suggested_tags_fusion.csv")
]

# === 自動選擇最合適的標籤來源 ===
for label, path in CANDIDATES:
    if os.path.exists(path):
        print(f"{label} → 採用 {path}")
        fusion_csv = path
        break
else:
    raise FileNotFoundError("❌ 找不到任何貼標輸出檔案")

df = pd.read_csv(fusion_csv)
updated = 0
skipped = 0

for _, row in df.iterrows():
    slug = row["slug"]
    md_path = os.path.join(MD_DIR, f"{slug}.md")
    if not os.path.exists(md_path):
        print(f"⚠️ 找不到檔案：{md_path}")
        skipped += 1
        continue

    tags = [t.strip() for t in str(row["tags_llm_filtered"]).split(",") if t.strip()]
    if not tags:
        print(f"⚠️ 無 tags 可寫入：{slug}")
        skipped += 1
        continue

    post = frontmatter.load(md_path)
    post["tags"] = tags

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))
    updated += 1

print(f"\n✅ 已寫入 tags 至 {updated} 篇文章，略過 {skipped} 篇")
