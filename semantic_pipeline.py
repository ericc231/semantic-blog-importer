# semantic_pipeline.py
import subprocess
import sys

steps = [
    ("🔁 融合貼標（KeyBERT + zh_embed）", "python extract_tags_fusion.py --mode union"),
    ("📈 高頻詞統計", "python generate_highfreq_words.py"),
    ("📊 TF-IDF 分數計算", "python generate_tfidf_scores.py"),
    ("✍️ 詞性標註", "python generate_pos_dict.py"),
    ("✨ 更新語意過渡詞", "python update_generic_transitions.py"),
    ("🤖 LLM 標籤語意審查", "python llm_reviewer.py"),
    ("🧽 根據 LLM 清理語助詞與語意弱詞", "python review2filter.py"),
    ("📝 寫入 Markdown metadata", "python write_back_tags.py"),
    ("📤 匯出 Notion 匯入格式", "python generate_notion_import_csv.py"),
    ("📊 標籤頻率統計與詞雲", "python tagging_report.py"),
    ("📈 語意相似度熱度圖", "python similarity_heatmap.py"),
    ("🧪 推敲語助詞後綴候選", "python generate_suffixes_from_corpus.py"),
    ("🎯 後綴品質評估排序", "python suffix_quality_ranker.py"),
    ("📊 後綴價值視覺化報表", "python suffix_dashboard.py")
]

print("🚀 開始執行 Semantic Pipeline...\n")

for label, cmd in steps:
    print(f"{label} → {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ 發生錯誤：{cmd}")
        sys.exit(1)
    print("✅ 完成\n")

print("🎉 所有步驟完成！請查看 tagging_report/ 與 tagging_qc_summary.md 檢視 QA 結果 📂✅")
