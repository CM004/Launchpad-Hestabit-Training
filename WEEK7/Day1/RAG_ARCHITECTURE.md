# RAG System Architecture

## Overview
This RAG (Retrieval-Augmented Generation) system consists of two main pipelines: Ingestion Pipeline (processes documents and builds searchable index) and Query Pipeline (retrieves relevant context and generates responses) [web:70][web:71].

## Project Structure
- src/
  - data/
    - raw/ (Original documents: PDF, TXT, CSV, DOCX)
    - cleaned/ (Loaded documents as JSON)
    - chunks/ (Chunked documents as JSON)
  - embeddings/
    - embedder.py (Generate embeddings)
    - embeddings.npy (Stored embeddings)
  - vectorstore/
    - indexing.py (Build FAISS index)
    - faiss.index (Vector database)
  - retriever/
    - query_engine.py (Query + LLM response)
  - utils/
    - loader.py (Load documents)
    - chunker.py (Chunk documents)
  - pipelines/
    - ingest.py (End-to-end ingestion)

## Ingestion Pipeline

### Step 1: Document Loading
File: src/utils/loader.py
Loads documents from src/data/raw/ supporting PDF, TXT, CSV, and DOCX formats [web:73]. Extracts text content and saves to src/data/cleaned/documents.json.

### Step 2: Text Chunking
File: src/utils/chunker.py
Reads from src/data/cleaned/documents.json and splits text using RecursiveCharacterTextSplitter with chunk size of 800 characters and overlap of 200 [web:72]. Preserves source metadata and saves to src/data/chunks/chunks.json.

### Step 3: Embedding Generation
File: src/embeddings/embedder.py
Reads chunks from src/data/chunks/chunks.json and uses sentence-transformers model to convert text to vector embeddings [web:75]. Saves to src/embeddings/embeddings.npy.

### Step 4: Index Building
File: src/vectorstore/indexing.py
Loads embeddings from src/embeddings/embeddings.npy and creates FAISS index for fast similarity search [web:71]. Saves to src/vectorstore/faiss.index.

## Query Pipeline
File: src/retriever/query_engine.py
User inputs query, query converted to embedding, FAISS searches for top-k similar chunks, retrieved chunks plus query sent to LLM, and LLM generates contextual response [web:72][web:74].

## Running the System

Full Ingestion:
python src/pipelines/ingest.py

Query:
python src/retriever/query_engine.py

## Key Components
- Document Loader: LangChain for multi-format document parsing
- Text Splitter: RecursiveCharacterTextSplitter for semantic chunking
- Embedder: sentence-transformers for vector representation
- Vector DB: FAISS for fast similarity search
- LLM: Groq/OpenAI for response generation

## Data Flow
Raw Docs → Loader → Cleaned JSON → Chunker → Chunks JSON → Embedder → Embeddings → FAISS Index → User Query → Retriever → Context → LLM → Response [web:70][web:79]

## Configuration
- Chunk Size: 800 characters
- Chunk Overlap: 200 characters
- Top-K Retrieval: 3-5 chunks
- Embedding Model: all-MiniLM-L6-v2
- Vector DB: FAISS with L2 distance
