# suffix_tool.py
import argparse
import pandas as pd
import os

SUFFIX_CSV = "tagging_report/suffix_quality_scores.csv"
SUFFIX_TXT = "config/suffixes.txt"

def load_existing_suffixes() -> set:
    return set(line.strip() for line in open(SUFFIX_TXT, encoding="utf-8") if line.strip()) if os.path.exists(SUFFIX_TXT) else set()

def save_suffixes(suffixes: set):
    with open(SUFFIX_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(suffixes)))

def recommend_top_n(n: int):
    df = pd.read_csv(SUFFIX_CSV)
    print(f"\n🔍 推薦剃除價值 Top {n} 後綴：\n")
    for i, row in enumerate(df.sort_values("score", ascending=False).head(n).itertuples(), 1):
        print(f"{i:2}. {row.suffix:<10} Score: {row.score:<6}  TF-IDF: {row.avg_tfidf:<6}  次數: {row.count}")

def approve_top_n(n: int, dry_run=False):
    existing = load_existing_suffixes()
    df = pd.read_csv(SUFFIX_CSV)
    top_suffixes = set(df.sort_values("score", ascending=False).head(n)["suffix"])
    new_suffixes = top_suffixes - existing
    combined = sorted(existing | new_suffixes)

    if not new_suffixes:
        print("✅ 前 N 後綴已全部在 suffixes.txt 中，無需更新")
        return

    if dry_run:
        print("📝 [Dry-run] 將新增以下後綴：")
        for s in sorted(new_suffixes):
            print(f"  - {s}")
    else:
        save_suffixes(set(combined))
        print(f"✅ 已將 {len(new_suffixes)} 個後綴加入 `suffixes.txt`")

def show_stats():
    df = pd.read_csv(SUFFIX_CSV)
    existing = load_existing_suffixes()
    in_list = df[df["suffix"].isin(existing)]
    out_list = df[~df["suffix"].isin(existing)]
    print("📊 後綴治理狀況統計：")
    print(f"- 🔹 總後綴數        ：{len(df)}")
    print(f"- ✅ 已啟用後綴    ：{len(in_list)}")
    print(f"- 🔍 剩餘候選      ：{len(out_list)}")
    print(f"- 🎯 已啟用平均得分：{round(in_list['score'].mean(), 3) if not in_list.empty else '—'}")
    print(f"- 📉 候選平均得分  ：{round(out_list['score'].mean(), 3) if not out_list.empty else '—'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="語助詞治理小工具 suffix_tool.py")
    parser.add_argument("--recommend-top", type=int, help="列出前 N 個推薦剃除後綴")
    parser.add_argument("--approve-top", type=int, help="將前 N 個後綴加入 suffixes.txt")
    parser.add_argument("--dry-run", action="store_true", help="與 --approve-top 搭配，僅顯示不寫入")
    parser.add_argument("--show-stats", action="store_true", help="顯示後綴治理統計資訊")

    args = parser.parse_args()

    if args.recommend_top:
        recommend_top_n(args.recommend_top)
    if args.approve_top:
        approve_top_n(args.approve_top, dry_run=args.dry_run)
    if args.show_stats:
        show_stats()
    if not any(vars(args).values()):
        parser.print_help()
