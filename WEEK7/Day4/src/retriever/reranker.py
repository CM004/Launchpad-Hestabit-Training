from sentence_transformers import CrossEncoder
import numpy as np

model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, docs, top_k=5):
    scores = model.predict([[query, d.page_content] for d in docs])
    top = np.argsort(scores)[::-1][:top_k]
    return [docs[i] for i in top]
