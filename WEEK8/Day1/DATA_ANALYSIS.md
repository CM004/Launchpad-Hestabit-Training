# Week-8 Day 1 – Dataset Processing Summary

## Overview
Dataset processing pipeline for a 2,000-sample instruction-tuning dataset in the Computer Science / Coding domain (instruction–input–output triples in JSONL format).

***

## File Summaries

### 1. `coding_raw_2000.jsonl` – Raw Dataset
Purpose: Base instruction-tuning dataset for TinyLlama fine-tuning.

- Total samples: 2,000
- Format: JSONL, one JSON object per line with fields: `instruction`, `input`, `output`

Task types included:

| Type        | Approx. Count | Description                                           |
|-------------|---------------|-------------------------------------------------------|
| QA          | ~700          | Code generation, coding questions, concept explainer  |
| Reasoning   | ~600          | Step-by-step code / algorithm explanations            |
| Extraction  | ~700          | Extract function names, parameters, details from code |

***

### 2. `utils/data_cleaner.py` – Cleaning, Token Stats, Split
Purpose: Clean the raw dataset, compute token statistics, remove outliers, and create train/validation splits.

Configuration:
- Input: `data/raw/coding_raw_2000.jsonl`  
- Output train file: `data/train.jsonl`  
- Output val file: `data/val.jsonl`  
- Train/Val ratio: 80/20 split (1,600 train / 400 val)
- Tokenizer for analysis: `tiktoken` with `cl100k_base` encoding
- Max tokens per sample: 2,000 (filter upper outliers)

Cleaning and filtering criteria:
1. Valid JSON line (invalid JSON lines are skipped).  
2. Non-empty `instruction` and `output`.  
3. Whitespace stripped from `instruction`, `input`, and `output`.  
4. Token length computed as  
   `len(instruction) + len(input) + len(output)` in `cl100k_base` tokens.  
5. Keep only samples with total tokens ≤ 2,000 and with instruction/output token counts > 0.  

Outputs:
- `data/train.jsonl`: 1,600 training samples after cleaning and filtering.  
- `data/val.jsonl`: 400 validation samples after cleaning and filtering.  
- Console stats (example run):  
   ![alt text](<Screenshot from 2026-01-12 02-47-50.png>)

***

### 3. Token Length Analysis and Distribution Graphs
Purpose: Understand token length distribution and verify suitability for TinyLlama context.

VS Code side (using `tiktoken`):
- Token length analysis integrated into `data_cleaner.py`.  
- Stats printed to console: total samples, train/val sizes, avg/max/min tokens.  
- Histogram of token lengths saved to:  
  `analysis/token_distribution.png`.  

Colab side (verification):
- Loaded `train.jsonl` and computed token lengths using both:  
  - TinyLlama `AutoTokenizer` (for model-view tokens).  
  - `tiktoken` `cl100k_base` (to match VS Code results).  
- Verified that `tiktoken`-based averages in Colab match VS Code (around 75 tokens on average).  

***
