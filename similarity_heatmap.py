# similarity_heatmap.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from semantic_distance import get_similarity
import os

INPUT_CSV = "dataset/suggested_tags_fusion.csv"
OUT_PATH = "tagging_report/tag_similarity_heatmap.png"
THRESHOLD_LINE = 0.2  # 可與 config.yaml 對齊

os.makedirs("tagging_report", exist_ok=True)

df = pd.read_csv(INPUT_CSV)
rows = []

for _, row in df.iterrows():
    slug = row["slug"]
    title = str(row["title"])
    tags = [t.strip() for t in str(row["tags_merged"]).split(",") if t.strip()]
    for tag in tags:
        sim = get_similarity(tag, title)
        rows.append({
            "slug": slug,
            "title": title,
            "tag": tag,
            "similarity": round(sim, 4)
        })

df_sim = pd.DataFrame(rows)
df_pivot = df_sim.pivot_table(index="slug", columns="tag", values="similarity", aggfunc="first").fillna(0)

plt.figure(figsize=(max(10, len(df_pivot.columns)//2), max(6, len(df_pivot)//2)))
sns.heatmap(df_pivot, annot=False, cmap="YlGnBu", vmin=0, vmax=1, cbar_kws={'label': 'Similarity'})
plt.axhline(y=THRESHOLD_LINE, color='red', linestyle='--', linewidth=1)
plt.title("🧠 Tag-to-Title Semantic Similarity Heatmap")
plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300)
plt.close()

print(f"✅ Heatmap 輸出完成 → {OUT_PATH}")
