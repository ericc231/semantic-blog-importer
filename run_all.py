from blog_loader.notion_loader import load_notion_export
import os
import shutil

OUTPUT_DIR = "docs/blogs"

def main():
    # 清除舊資料
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 載入 Notion 匯出資料
    load_notion_export(
        input_folder="input/notion_export",
        output_folder=OUTPUT_DIR
    )

    print(f"✅ 部落格文章已匯出至：{OUTPUT_DIR}")

if __name__ == "__main__":
    main()
