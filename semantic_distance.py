# semantic_distance.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

# ✅ 載入模型（lazy loading 避免重複初始化）
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def get_similarity(tag: str, title: str) -> float:
    tag = tag.strip()
    title = title.strip()
    if not tag or not title:
        return 0.0
    model = get_model()
    embeddings = model.encode([tag, title], convert_to_tensor=False, normalize_embeddings=True)
    return float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0])
