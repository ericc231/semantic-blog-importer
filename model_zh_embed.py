# model_zh_embed.py
import torch
import jieba
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "bert-base-chinese"

# === 裝置選擇：CUDA → MPS → CPU ===
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("✅ 使用 GPU：CUDA")
elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
    device = torch.device("mps")
    print("🍎 使用 GPU：Apple MPS")
else:
    device = torch.device("cpu")
    print("💻 使用 CPU：未偵測到可用 GPU")

# === 載入模型與 tokenizer ===
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME).to(device)
model.eval()

@torch.no_grad()
def embed_text(text: str) -> torch.Tensor:
    encoded = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=256,
        padding="max_length"
    ).to(device)

    output = model(**encoded)
    cls_vec = output.last_hidden_state[:, 0, :]  # 取 [CLS] 向量
    return cls_vec.cpu()  # 回傳 CPU tensor，供 numpy 使用

def extract_zh_keywords(text: str, top_n=5) -> list:
    words = list(set(jieba.lcut(text)))
    words = [w for w in words if len(w.strip()) >= 2]

    if not words:
        return []

    text_vec = embed_text(text).numpy()
    word_vecs = [embed_text(w).numpy()[0] for w in words]
    scores = cosine_similarity(text_vec, word_vecs)[0]

    ranked = sorted(zip(words, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]
