# clean.py
import os
import shutil

TARGETS = [
    "dataset/suggested_tags_fusion.csv",
    "dataset/suggested_tags_fusion_llm_filtered.csv",
    "dataset/tag_review_llm.csv",
    "dataset/Notion_import_ready.csv",
    "dataset/write_log.csv",  # 若 write_back_tags 產生變動紀錄
    "dataset/articles.csv",
    "config/highfreq_words.csv",
    "config/tfidf_scores.csv",
    "config/pos_dict.json",
    "config/stopwords_full.txt",
    "config/stopwords_traditional.txt",
    "config/generic_transitions.txt",
    "config/suffix_candidates.csv",
    "tagging_report",  # 資料夾：報表輸出
    "exported_md",  # 資料夾：Markdown 檔案
    "assets/r2",  # 資料夾：R2 上傳的資源
    "assets/pages",  # 資料夾：Markdown 頁面
    "tagging_qc_summary.md"  # 若有 QA 紀錄
]

def remove(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"🧹 移除資料夾：{path}")
    elif os.path.isfile(path):
        os.remove(path)
        print(f"🗑️ 移除檔案：{path}")
    else:
        print(f"⚠️ 找不到目標：{path}")

if __name__ == "__main__":
    print("🧼 清理語意貼標相關產出物...\n")
    for target in TARGETS:
        remove(target)
    print("\n✅ 清理完成！你的專案資料夾已回到初始狀態。")
