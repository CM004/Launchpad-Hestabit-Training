## MULTIMODAL-RAG

## Overview  
Day 3 extends the RAG system to support images using CLIP for embeddings and BLIP for captions. The system enables text-to-image and image-to-image semantic search over an enterprise image dataset.

## Project Structure  
- src/  
  - data/  
    - images/ (raw images in nested EnterpriseRAG_2025_02_markdown folders)  
    - images_metadata/  
      - images.json (metadata: filename, folder, path, OCR text, BLIP caption)  
  - embeddings/  
    - image_embeddings/ (CLIP image embeddings as .npy files)  
    - clip_embedder.py (CLIP image + text encoders)  
    - blip_captioner.py (BLIP image captioning)  
  - vectorstore/  
    - image_index.faiss (FAISS index over image embeddings)  
  - pipelines/  
    - image_ingest.py (image OCR, captioning, embedding, metadata generation)  
  - retriever/  
    - image_search.py (text/image search over image index)

## Image Ingestion Pipeline (image_ingest.py)

Step 1: Image Loading  
Scans src/data/images/EnterpriseRAG_2025_02_markdown, iterates over nested folders, and loads all .jpg/.jpeg/.png images as RGB using Pillow.

Step 2: OCR and Captioning  
For each image, extracts visible text with Tesseract OCR and generates a natural language caption with BLIP. Both OCR text and caption are stored in images.json as metadata.

Step 3: Embedding Generation  
Uses CLIP image encoder to convert each image into a 512‑dimensional float32 embedding vector. Each embedding is saved as a separate .npy file in src/embeddings/image_embeddings/.

Step 4: Metadata Storage  
For every processed image, stores filename, folder name, full path, truncated OCR text, and BLIP caption in src/data/images_metadata/images.json.

## Indexing and Retrieval

Index Building (image_search.py)  
Loads images.json, reads corresponding .npy embeddings, stacks them into a NumPy array of shape (num_images, 512), and builds a FAISS IndexFlatL2 index. The index is saved to src/vectorstore/image_index.faiss for reuse.

Query Flow (image_search.py)  
- Text search: converts query text to a 512‑dim CLIP text embedding, searches FAISS for top‑k nearest image embeddings, and returns folder, filename, and caption for each result.  
- Image search: converts a query image to a 512‑dim CLIP image embedding, searches FAISS for the most similar images, and returns their metadata.

## Running

Ingest images and build embeddings:  
python src/pipelines/image_ingest.py  

Search images (text or image mode):  
python src/retriever/image_search.py

## Screenshots

![alt text](<Screenshot from 2026-01-06 12-33-09.png>)

![alt text](<Screenshot from 2026-01-06 17-51-35.png>)