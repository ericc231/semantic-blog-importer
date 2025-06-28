# tag_cleaner.py
import os
import re
import requests
import yaml
from collections import Counter
from opencc import OpenCC
from semantic_distance import get_similarity

# === 組態與路徑 ===
CONFIG_DIR = "config"
#CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")
CONFIG_PATH = "config.yaml"
STOPWORDS_URL = "https://raw.githubusercontent.com/CharyHong/Stopwords/main/stopwords_full.txt"
STOPWORDS_S_PATH = os.path.join(CONFIG_DIR, "stopwords_full.txt")
STOPWORDS_T_PATH = os.path.join(CONFIG_DIR, "stopwords_traditional.txt")
GENERIC_PATH = os.path.join(CONFIG_DIR, "generic_transitions.txt")
SUFFIXES_PATH = os.path.join(CONFIG_DIR, "suffixes.txt")

# === 載入參數 ===
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
STOPWORDS_URL = config.get("stopwords", {}).get("url", STOPWORDS_URL)
semantic_cfg = config.get("semantics", {})
USE_EMBEDDING = semantic_cfg.get("use_embedding_similarity", True)
SIM_THRESHOLD = semantic_cfg.get("similarity_threshold", 0.2)

# === 停用詞下載與轉換 ===
def prepare_stopwords():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    if not os.path.exists(STOPWORDS_S_PATH):
        print("🌐 下載簡體停用詞...")
        r = requests.get(STOPWORDS_URL)
        with open(STOPWORDS_S_PATH, "w", encoding="utf-8") as f:
            f.write(r.text)
    if not os.path.exists(STOPWORDS_T_PATH):
        print("🔁 轉換為繁體...")
        cc = OpenCC("s2t")
        with open(STOPWORDS_S_PATH, "r", encoding="utf-8") as f:
            simplified = [line.strip() for line in f if line.strip()]
        traditional = sorted(set(cc.convert(w) for w in simplified))
        with open(STOPWORDS_T_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(traditional))

def load_list(path) -> set:
    return set(line.strip() for line in open(path, encoding="utf-8") if line.strip()) if os.path.exists(path) else set()

# === 初始化 ===
prepare_stopwords()
STOPWORDS = load_list(STOPWORDS_T_PATH)
GENERIC = load_list(GENERIC_PATH)
SUFFIXES = load_list(SUFFIXES_PATH)

# === 清除後綴詞（外部定義）===
def suffix_remover(tag: str) -> str:
    for suffix in SUFFIXES:
        if tag.endswith(suffix) and len(tag) > len(suffix) + 1:
            return tag[: -len(suffix)]
    return tag

# === 核心判定 ===
def is_noisy(tag: str, title: str = "") -> bool:
    tag = tag.strip()
    tag = suffix_remover(tag)
    return (
        not tag or
        tag in STOPWORDS or
        tag in GENERIC or
        len(tag) > 12 or
        " " in tag or
        bool(re.search(r"[！？。．～‧,，\n]", tag)) or
        (USE_EMBEDDING and title and get_similarity(tag, title) < SIM_THRESHOLD)
    )

def clean_tags(tags: list[str], title: str = "", removed_counter: Counter = None) -> list[str]:
    cleaned = []
    for t in tags:
        t = suffix_remover(t)
        if is_noisy(t, title):
            if removed_counter is not None:
                removed_counter[t] += 1
        else:
            cleaned.append(t)
    return cleaned
