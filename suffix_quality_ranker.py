# suffix_quality_ranker.py
import pandas as pd
import os

CANDIDATES_CSV = "config/suffixes_candidates.csv"
TFIDF_CSV = "config/tfidf_scores.csv"
LLM_REVIEW = "dataset/tag_review_llm.csv"
OUT_PATH = "tagging_report/suffix_quality_scores.csv"

os.makedirs("tagging_report", exist_ok=True)

df_suffix = pd.read_csv(CANDIDATES_CSV)
df_tfidf = pd.read_csv(TFIDF_CSV)
df_llm = pd.read_csv(LLM_REVIEW)

# 建構參照表
tfidf_dict = dict(zip(df_tfidf["word"], df_tfidf["tfidf"]))
filtered_tags = set(
    row["tag"] for _, row in df_llm.iterrows()
    if str(row.get("should_filter", "")).lower() in {"true", "yes", "1"}
)

# 分析每個 suffix 的語意得分
results = []
for _, row in df_suffix.iterrows():
    suffix = str(row["suffix"])
    freq = int(row["count"])
    tfidfs, filtered_count = [], 0

    for word in df_tfidf["word"]:
        if word.endswith(suffix) and len(word) > len(suffix) + 1:
            tfidfs.append(tfidf_dict.get(word, 0))
            if word in filtered_tags:
                filtered_count += 1

    avg_tfidf = sum(tfidfs) / len(tfidfs) if tfidfs else 0.0
    score = (freq / 10) - avg_tfidf * 3 + filtered_count * 0.5  # 綜合剃除價值

    results.append({
        "suffix": suffix,
        "count": freq,
        "examples": ", ".join([w for w in tfidf_dict if w.endswith(suffix)][:5]),
        "avg_tfidf": round(avg_tfidf, 4),
        "in_filtered_tags": filtered_count,
        "score": round(score, 4)
    })

pd.DataFrame(results).sort_values("score", ascending=False).to_csv(
    OUT_PATH, index=False, encoding="utf-8-sig"
)
print(f"✅ 後綴品質分析已輸出：{OUT_PATH}")
