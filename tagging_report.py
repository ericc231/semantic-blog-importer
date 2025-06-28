# tagging_report.py
import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

INPUT_CANDIDATES = [
    "dataset/suggested_tags_fusion_llm_filtered.csv",
    "dataset/suggested_tags_fusion.csv",
    "dataset/suggested_tags.csv"
]
TAG_COLUMNS = ["tags_llm_filtered", "tags_merged", "suggested_tags", "tags_zh"]

os.makedirs("tagging_report", exist_ok=True)

# 選擇現有輸入檔案
for path in INPUT_CANDIDATES:
    if os.path.exists(path):
        INPUT_CSV = path
        break
else:
    raise FileNotFoundError("❌ 找不到任何可用的貼標檔案")

df = pd.read_csv(INPUT_CSV)

# 選擇現有欄位
for col in TAG_COLUMNS:
    if col in df.columns:
        TAG_FIELD = col
        break
else:
    raise ValueError("❌ 找不到任何標籤欄位，如 tags_merged、tags_zh 等")

# 統計標籤頻率
tags = []
for entry in df[TAG_FIELD].dropna():
    tags.extend([t.strip() for t in str(entry).split(",") if t.strip()])

counter = Counter(tags)
df_out = pd.DataFrame(counter.most_common(100), columns=["tag", "count"])
df_out.to_csv("tagging_report/tag_stats.csv", index=False, encoding="utf-8-sig")

# 畫詞雲
wc = WordCloud(font_path="fonts/NotoSansTC-Regular.ttf", background_color="white", width=800, height=600)
wc.generate_from_frequencies(counter)
wc.to_file("tagging_report/tag_wordcloud.png")

print(f"✅ 分析完成：\n- Top 標籤 CSV → tagging_report/tag_stats.csv\n- 詞雲圖 → tagging_report/tag_wordcloud.png")
