## Retrieval Strategies – Day 2

## Overview  
- Day 2 adds a smarter retrieval layer on top of the Day 1 RAG system.  
- Goal: get more relevant chunks, cut down hallucinations, and always know exactly which file and chunk each answer came from.

## Project Structure (Day 2)  
- `src/retriever/hybrid_retriever.py`  
  - Hybrid search using BM25 + FAISS + RRF.  
- `src/retriever/reranker.py`  
  - Cross-encoder based reranking of retrieved chunks.  
- `src/pipelines/context_builder.py`  
  - Orchestrates retrieval + reranking and builds the final context + sources list.  

Day 1 (loader, chunker, embedder, indexing, query_engine) stays the same and still powers the basic FAISS-only query flow.

## Hybrid Retrieval (BM25 + FAISS + RRF)  
**File:** `src/retriever/hybrid_retriever.py`  

- Reads chunks from `src/data/chunks/chunks.json` (`text`, `source`, `chunk_id`).  
- Builds two retrievers on the same data:  
  - BM25 retriever for keyword / exact string match (IDs, names, URLs, etc.).  
  - FAISS retriever using `all-MiniLM-L6-v2` embeddings for semantic search.  
- For each query:  
  - BM25 is called with `bm25.k = 25`.  
  - FAISS is called with `search_kwargs={"k": 25}`.  
- Both ranked lists are merged with **Reciprocal Rank Fusion (RRF)**:  
  - Each document gets a score of `1 / (60 + rank)` every time it appears in a list.  
  - Scores from BM25 and FAISS are added together.  
  - Duplicates are removed by using `page_content` as the key.  
  - `retrieve(query, k)` finally returns the top `k` documents after this fused scoring (for Day 2, upstream asks for 50).

## Cross-Encoder Reranking  
**File:** `src/retriever/reranker.py`  

- Uses `cross-encoder/ms-marco-MiniLM-L-6-v2`.  
- Takes the candidate docs from `retrieve(query, k=50)`.  
- Builds `[query, doc.page_content]` pairs and scores them with the cross-encoder.  
- Sorts documents by this score and returns the top `top_k` (fixed to 5).  
- Idea: BM25 + FAISS + RRF gives a good candidate pool (high recall), and the cross-encoder cleans it up and keeps only the best few (high precision).

## Context Builder  
**File:** `src/pipelines/context_builder.py`  

- Calls `retrieve(query, k=50)` to get a wide set of candidates.  
- Calls `rerank(query, docs, top_k=5)` to pick the 5 most relevant chunks.  
- Builds the final context string like:  
  - `[1] <chunk 1 text>`  
  - `[2] <chunk 2 text>`  
  - … up to `[5]`, joined with blank lines.  
- Returns a dictionary with:  
  - `context`: all 5 chunks formatted and ready to send to the LLM.  
  - `sources`: a list of `{"source": <filename>, "chunk_id": <chunk_id>}` so each chunk can be traced back to the original Day 1 `chunks.json` entry. 

## Integration with Query Engine
**File:** `src/retriever/query_engine.py`

- Uses build_context(query, k=5) instead of Day 1's simple FAISS-only retrieval.
- Sends formatted context + query to LLM.
- Returns answer + traceable sources.
- 3-4 minutes (building BM25 + FAISS indexes).

![alt text](<Screenshot from 2026-01-05 18-47-55.png>)

## To see raw context without LLM 
- run with `python src/pipelines/context_builder.py`:  
  - Asks only for the query (k is fixed to 5 inside the script).  
  - Prints the `CONTEXT` section (5 numbered chunks).  
  - Prints the `SOURCES` section showing which file and chunk_id each of those 5 chunks came from.

![alt text](<Screenshot from 2026-01-05 18-41-52.png>)

## Benefits
1. Higher precision (keyword + semantic combined)
2. Lower hallucination (reranked, relevant context)
3. Fully traceable (source file + chunk_id per chunk)
4. Fast queries (50→5 filtering reduces noise)