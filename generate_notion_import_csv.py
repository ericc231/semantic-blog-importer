# generate_notion_import_csv.py
import os
import frontmatter
import pandas as pd

MD_DIR = "exported_md"
FUSION_CSV = "dataset/suggested_tags_fusion.csv"
OUTPUT_CSV = "dataset/Notion_import_ready.csv"

# 建立 slug → merged tag map
tag_map = {}
fusion_df = pd.read_csv(FUSION_CSV)
for _, row in fusion_df.iterrows():
    slug = row["slug"]
    tags = [t.strip() for t in str(row["tags_merged"]).split(",") if t.strip()]
    tag_map[slug] = tags

rows = []
for filename in os.listdir(MD_DIR):
    if not filename.endswith(".md"):
        continue
    slug = filename[:-3]
    path = os.path.join(MD_DIR, filename)
    post = frontmatter.load(path)

    title = post.get("title", slug)
    date = post.get("date", "")
    content = post.content.strip()
    final_tags = tag_map.get(slug, post.get("tags", []))

    rows.append({
        "title": title,
        "slug": slug,
        "date": date,
        "tags": ", ".join(final_tags),
        "content": content
    })

pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"📤 已匯出 Notion 匯入檔案：{OUTPUT_CSV}（{len(rows)} 篇）")
