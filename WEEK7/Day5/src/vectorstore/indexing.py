import json
import numpy as np
import faiss
from pathlib import Path

embeddings = np.load("src/embeddings/embeddings.npy").astype('float32') #load embeddings and chunks
chunks = json.load(open("src/data/chunks/chunks.json"))

dimension = embeddings.shape[1] #build FAISS index
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

Path("src/vectorstore").mkdir(exist_ok=True) #save
faiss.write_index(index, "src/vectorstore/index.faiss")
json.dump(chunks, open("src/vectorstore/metadata.json", "w"), indent=2)

print("Index built:", index.ntotal," vectors, dimension ",dimension)
