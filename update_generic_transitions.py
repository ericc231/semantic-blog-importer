# update_generic_transitions.py
import os
import yaml
import pandas as pd
import json

# 路徑設定
FREQ_CSV = "config/highfreq_words.csv"
TFIDF_CSV = "config/tfidf_scores.csv"
POS_JSON = "config/pos_dict.json"
GENERIC_PATH = "config/generic_transitions.txt"
CONFIG_PATH = "config.yaml"

# 載入 config.yaml
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
cfg = config.get("transitions", {})
TOP_N = cfg.get("top_n_freq", 150)
TFIDF_THRESHOLD = cfg.get("tfidf_threshold", 0.12)
ALLOWED_POS = set(cfg.get("allowed_pos", ["n", "nr", "ns", "nt", "nz"]))

# 載入資料
df_freq = pd.read_csv(FREQ_CSV).head(TOP_N)
tfidf_dict = {}
pos_dict = {}

if os.path.exists(TFIDF_CSV):
    df_tfidf = pd.read_csv(TFIDF_CSV)
    tfidf_dict = dict(zip(df_tfidf["word"], df_tfidf["tfidf"]))

if os.path.exists(POS_JSON):
    with open(POS_JSON, "r", encoding="utf-8") as f:
        pos_dict = json.load(f)

existing = set()
if os.path.exists(GENERIC_PATH):
    with open(GENERIC_PATH, "r", encoding="utf-8") as f:
        existing = set(line.strip() for line in f if line.strip())

# 判斷邏輯
def is_generic_by_semantics(word: str) -> bool:
    tfidf = tfidf_dict.get(word, 1.0)
    pos = pos_dict.get(word, "").lower()

    if tfidf < TFIDF_THRESHOLD:
        return True
    if pos and pos not in ALLOWED_POS:
        return True
    return False

# 執行判斷
candidates = [w.strip() for w in df_freq["word"] if isinstance(w, str) and w.strip()]
new_words = [w for w in candidates if w not in existing and is_generic_by_semantics(w)]
combined = sorted(existing.union(new_words))

with open(GENERIC_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(combined))

print(f"✅ 新增 {len(new_words)} 個過渡詞 → {GENERIC_PATH}")
