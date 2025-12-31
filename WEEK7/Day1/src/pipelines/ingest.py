import os
import sys
sys.path.append('src')

print("Starting RAG Pipeline\n")

print("Step 1: Loading documents...")
import utils.loader
print("Documents loaded\n")

print("Step 2: Chunking documents...")
import utils.chunker
print("Chunks created\n")

print("Step 3: Generating embeddings...")
import embeddings.embedder
print("Embeddings created\n")

print("Step 4: Building FAISS index...")
import vectorstore.indexing
print("Vector DB initialized\n")

print("Pipeline Complete\n")
print("Now you can query using: python src/retriever/query_engine.py")
