# upload_to_pages.py
import shutil
import os
import yaml

# 讀取 config.yaml 設定
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def upload_to_pages(filename: str, src_path: str):
    """將圖片複製到 GitHub Pages 的資料夾（如已在正確位置則略過）"""
    dst_dir = config["pages_root"]
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, filename)

    # ⚠️ 防呆：避免來源與目標為同一路徑
    if os.path.abspath(src_path) == os.path.abspath(dst_path):
        print(f"⚠️ [跳過] 圖片已在目標資料夾中：{dst_path}")
        return

    # 執行複製
    shutil.copy2(src_path, dst_path)
    print(f"📁 圖片複製完成：{src_path} → {dst_path}")
