# model_ckip.py
print("🔧 model_ckip.py 已成功載入")
import torch
from sklearn.metrics.pairwise import cosine_similarity
from ckip_transformers.nlp import CkipWordSegmenter, CkipSentenceEncoder

ws_driver = CkipWordSegmenter(device=-1)      # CPU 模式
encoder = CkipSentenceEncoder(device=-1)

def extract_ckip_keywords(text: str, top_n=5):
    # 中文斷詞
    tokens = ws_driver([text])[0]
    candidates = list(set(tokens))
    candidates = [t for t in candidates if len(t) >= 2]

    # 向量化：整體文本 vs. 每個詞
    text_vec = encoder([text])[0]
    word_vecs = encoder(candidates)

    # 計算語意相似度
    scores = cosine_similarity([text_vec], word_vecs)[0]
    sorted_pairs = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)

    return sorted_pairs[:top_n]

