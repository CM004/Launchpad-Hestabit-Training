# Week-8 Day 2 – LoRA / QLoRA Training

## Overview

Parameter-efficient fine-tuning of a 1.1B parameter language model using **LoRA with 4-bit QLoRA**, trained on the cleaned 2,000-sample instruction-tuning dataset prepared on Day 1. Training was performed on free Google Colab hardware (T4 GPU) with strict memory constraints.

---
## Dataset Configuration

### Data Sources
- **Training Data**: `/kaggle/input/instruct-dataset/train.jsonl`
- **Validation Data**: `/kaggle/input/instruct-dataset/val.jsonl`

### Data Format
The dataset follows an instruction-tuning format with three components:
- `instruction` - Task description
- `input` - Context or additional information
- `output` - Expected response

### Prompt Template
```
### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}
```

## Base Model

* Model: `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
* Architecture: Decoder-only Transformer
* Total parameters: ~1.1B
* Max context length: 2048 tokens

## Quantization

Purpose: Enable large-model training on limited GPU memory.

* Quantization method: 4-bit NF4 (BitsAndBytes)
* Compute dtype: FP16
* Double quantization: Enabled
* Memory reduction: ~75% vs FP32
* Result: Model fits comfortably on Tesla T4 (15 GB VRAM)

## Tokenization

### Tokenizer Configuration
- Uses the AutoTokenizer from the base model
- Truncation enabled at 512 tokens
- Labels created by copying input_ids for causal language modeling

---

## LoRA Configuration

Purpose: Train a minimal number of parameters while freezing the base model.

Configuration:

* Rank (r): 16
* Alpha: 32    
* Dropout: 0.05*
* Bias: None*
* Target modules:

  * `q_proj` - query 
  * `k_proj` - key
  * `v_proj` - value
  * `o_proj` - output
* Task type: Causal Language Modeling

Only LoRA adapter weights were marked trainable; all base model parameters remained frozen.

---

## Parameter Efficiency

| Component     | Parameters | Training Status |
| ------------- | ---------- | --------------- |
| Base Model    | ~1.10B     | Frozen          |
| LoRA Adapters | ~4.5M      | Trainable       |

* Trainable parameters: **0.41%**
* Frozen parameters: **99.59%**

This meets the assignment requirement of ~1% trainable parameters.

---

## Training Configuration

Purpose: Stable fine-tuning under memory and compute limits.

* Learning rate: 2e-4
* Batch size: 4
* Epochs: 3
* Optimizer: `paged_adamw_8bit`
* Precision: FP16
* Max sequence length: 512
* Gradient accumulation: 1

Memory optimizations used:

* 4-bit model loading
* LoRA adapters
* 8-bit optimizer
* Mixed precision training


---

## Dataset Usage

* Training file: `train.jsonl` (1,600 samples)
* Validation file: `val.jsonl` (400 samples)
* Domain: Computer Science / Coding instructions
* Format: Instruction–input–output JSONL

Preprocessing applied during training:

* Tokenization with TinyLlama tokenizer
* Chat template formatting
* EOS token appended
* Truncation to 512 tokens

---

## Training Outcome

* Training completed successfully for all 3 epochs
* Loss decreased consistently across epochs
* No OOM errors or instability observed
* Model converged within expected time (< 1 hour)

---

## Output Artifacts

Saved adapter directory:
- Saves LoRA adapter weights only (not the full model)
- Tokenizer configuration saved alongside adapters

```
adapters/coding-lora/
├── adapter_model.safetensors
├── adapter_config.json
├── tokenizer files
└── README.md
```

* Adapter size: ~20–50 MB
* Base model not duplicated
* Adapters are portable and reusable

---

## Training Process Summary

1. **Environment Setup** - Install required libraries
2. **Data Loading** - Load instruction dataset from JSONL files
3. **Tokenization** - Convert text to tokens with proper formatting
4. **Model Loading** - Load base model
5. **LoRA Application** - Apply LoRA adapters to target modules
6. **Training** - Fine-tune for 3 epochs with specified hyperparameters
7. **Save Adapters** - Export trained LoRA weights

