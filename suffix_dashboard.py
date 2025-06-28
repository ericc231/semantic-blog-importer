# suffix_dashboard.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
from adjustText import adjust_text
import matplotlib
import os

# === 字體設定 ===
FONT_PATH = "fonts/NotoSansTC-Regular.ttf"
font_manager.fontManager.addfont(FONT_PATH)
matplotlib.rcParams["font.family"] = "Noto Sans TC"
matplotlib.rcParams["axes.unicode_minus"] = False

# === 路徑設定 ===
CSV_PATH = "tagging_report/suffix_quality_scores.csv"
IMG_PATH = "tagging_report/suffix_dashboard.png"
SUMMARY_PATH = "tagging_qc_summary.md"
os.makedirs("tagging_report", exist_ok=True)

# === 讀取資料 ===
df = pd.read_csv(CSV_PATH)

# === 繪圖 ===
plt.figure(figsize=(11, 7))
sns.scatterplot(
    data=df,
    x="avg_tfidf",
    y="count",
    hue="score",
    size="in_filtered_tags",
    palette="coolwarm",
    sizes=(50, 250),
    legend="brief"
)

# 自動調整標籤位置與箭頭
texts = []
for _, row in df.sort_values("score", ascending=False).head(20).iterrows():
    texts.append(plt.text(row["avg_tfidf"], row["count"], row["suffix"], fontsize=9))

adjust_text(texts, arrowprops=dict(arrowstyle="->", color='gray', lw=0.5))

# 標題與軸
plt.title("🧠 後綴剃除價值圖（繁體中文支援）")
plt.xlabel("平均 TF-IDF（越低 → 越無資訊）")
plt.ylabel("語料中出現次數")
plt.grid(True)
plt.tight_layout()
plt.savefig(IMG_PATH, dpi=300)
plt.close()

print(f"✅ 圖表已輸出：{IMG_PATH}")

# === 摘要寫入 tagging_qc_summary.md ===
top_suffixes = df.sort_values("score", ascending=False).head(10)

with open(SUMMARY_PATH, "a", encoding="utf-8") as f:
    f.write("## 🔍 後綴治理評估摘要\n\n")
    f.write(f"- 🔢 分析後綴數量：{len(df)}\n")
    f.write("- 📈 高剃除價值 TOP 10 後綴：\n\n")
    for _, row in top_suffixes.iterrows():
        f.write(f"  - `{row['suffix']}`：分數 {row['score']}，TF-IDF {row['avg_tfidf']}，出現次數 {row['count']}\n")
    f.write(f"\n🖼️ 可視化圖表：`{IMG_PATH}`\n\n")
    f.write("---\n\n")

print(f"📝 摘要已寫入：{SUMMARY_PATH}")
