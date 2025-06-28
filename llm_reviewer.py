# llm_reviewer.py
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

CSV_PATH = "dataset/suggested_tags_fusion.csv"
OUTPUT_CSV = "dataset/tag_review_llm.csv"

MODEL_NAME = "uer/roberta-base-finetuned-chinanews-chinese"
classifier = pipeline("text-classification", model=MODEL_NAME, top_k=1)

df = pd.read_csv(CSV_PATH)
rows = []

print("🤖 LLM 正在審查標籤樣式與主題語意...\n")

for _, row in df.iterrows():
    slug = row["slug"]
    merged_tags = [t.strip() for t in str(row["tags_merged"]).split(",") if t.strip()]

    for tag in merged_tags:
        try:
            pred = classifier(tag)[0]
            label = pred["label"]
            score = pred["score"]
        except Exception as e:
            label, score = "error", 0.0

        rows.append({
            "slug": slug,
            "tag": tag,
            "predicted_label": label,
            "score": round(score, 3)
        })

pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
print(f"✅ LLM 分析完成 → {OUTPUT_CSV}")
