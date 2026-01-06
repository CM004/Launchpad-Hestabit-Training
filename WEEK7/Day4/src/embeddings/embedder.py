import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

chunks = json.load(open("src/data/chunks/chunks.json")) #load chunks
texts = [c["text"] for c in chunks]

embeddings = model.encode(texts, show_progress_bar=True) #generate embeddings

Path("src/embeddings").mkdir(exist_ok=True) #save embeddings
np.save("src/embeddings/embeddings.npy", embeddings)
json.dump(chunks, open("src/data/chunks/chunks.json", "w"), indent=2)

print("Saved embeddings: shape", embeddings.shape)
