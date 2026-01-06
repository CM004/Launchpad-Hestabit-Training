import os
import sys
sys.path.append('src')

import json
import numpy as np
from pathlib import Path
from embeddings.clip_embedder import embed_image, embed_text
import faiss

images_data = json.load(open("src/data/images_metadata/images.json"))
embeddings = []
filenames = []
folders = []

for img in images_data: 
    emb_path = f"src/embeddings/image_embeddings/image_{img['folder']}_{img['filename'].split('.')[0]}.npy"
    if Path(emb_path).exists():
        embeddings.append(np.load(emb_path).astype('float32'))  #loading embeddings(.npy/512 dim vectors) for indexing (32 bit floats)
        filenames.append(img['filename'])
        folders.append(img['folder'])

embeddings = np.array(embeddings) #stores list of embeddings to numpy array (2D array)
index = faiss.IndexFlatL2(embeddings.shape[1]) #creates empty L2 distance index for 512-dimensional vectors
index.add(embeddings) #builds internal data structures for fast similarity search

Path("src/vectorstore").mkdir(exist_ok=True)
faiss.write_index(index, "src/vectorstore/image_index.faiss") #save_index

def search_text(query, k=5):
    query_emb = embed_text(query).astype('float32').reshape(1, -1)
    _, idxs = index.search(query_emb, k)
    return [{"folder": folders[i], "file": filenames[i], "caption": images_data[i]["caption"]} for i in idxs[0]]

def search_image(image_path, k=5):  #retrieval-image
    query_emb = embed_image(image_path).astype('float32').reshape(1, -1) #image query-> clip image encoder-> embedding
    _, idxs = index.search(query_emb, k) #search in faiss index for top k nearest image embeddings ranked by L2 distances 
    return [{"folder": folders[i], "file": filenames[i], "caption": images_data[i]["caption"]} for i in idxs[0]] #returns image path and caption

if __name__ == "__main__":
    mode = input("Search by (text/image): ")
    query = input("Enter query: ") if mode == "text" else input("Enter image path: ")
    results = search_text(query) if mode == "text" else search_image(query)
    
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['folder']}] {r['file']} - {r['caption']}")
