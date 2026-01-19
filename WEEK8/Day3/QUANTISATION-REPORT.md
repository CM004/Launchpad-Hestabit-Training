# Model Quantization Pipeline

## Overview
This report documents the quantization pipeline that converts the fine-tuned LoRA model into multiple quantized formats for efficient deployment across different hardware configurations.

The pipeline merges a LoRA-fine-tuned TinyLlama model and exports it into multiple deployment-ready formats:
- Hugging Face FP16 / INT8 / INT4 (NF4)
- GGUF FP16 / Q8_0 / Q4_0

---

## Environment Setup

### Libraries Installed

- pip install -U transformers peft accelerate bitsandbytes datasets
- pip install llama-cpp-python


### Frameworks

* transformers
* peft
* bitsandbytes
* llama.cpp
* llama-cpp-python

---

## Base Configuration

### Model Details

* **Base Model**: TinyLlama/TinyLlama-1.1B-Chat-v1.0
* **Fine-tuning Method**: LoRA
* **LoRA Adapter Path**:
  `/content/drive/MyDrive/coding-lora`

### Output Root

```
/content/drive/MyDrive/Colab Notebooks/quantized
```

---

## Output Directory Structure

```
quantized/
├── merged-fp16/        # FP16 merged HF model
├── model-int8/         # INT8 HF model 
├── model-int4/         # INT4 NF4 HF model
├── model-f16.gguf      # GGUF FP16
├── model-q8_0.gguf     # GGUF Q8_0
└── model-q4_0.gguf     # GGUF Q4_0
```

---

## Quantization Workflow

1. Load base TinyLlama model in FP16
2. Merge LoRA adapters into base model
3. Save merged FP16 Hugging Face model
4. Quantize merged model to INT8 (bitsandbytes)
5. Quantize merged model to INT4 NF4 (bitsandbytes)
6. Convert merged FP16 model to GGUF (F16)
7. Quantize GGUF model to Q8_0
8. Quantize GGUF model to Q4_0
9. Measure disk sizes

---

## Stage 1: LoRA Merge (FP16)

**Purpose**
Create a standalone FP16 model by merging LoRA adapters into the base TinyLlama model.

**Process**

* Load base model in FP16
* Load LoRA adapters via `PeftModel`
* Merge adapters using `merge_and_unload()`
* Save model and tokenizer

**Output**

* Directory: `merged-fp16/`
* Precision: FP16 (16-bit floating point)
* Contents: Full model weights + tokenizer configuration
---

## Stage 2: INT8 Quantization (Hugging Face)

**Purpose**: Reduce model size by half with minimal quality degradation

**Configuration**

```python
BitsAndBytesConfig(load_in_8bit=True)
```

**Process**

* Load merged FP16 model
* Apply 8-bit quantization using bitsandbytes
* Save quantized model

**Output**

* Directory: `model-int8/`
* Precision: INT8

---

## Stage 3: INT4 Quantization (NF4)

**Purpose**: Maximum size reduction with acceptable quality loss

**Configuration**

```python
BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",          #optimized 4-bit format
    bnb_4bit_compute_dtype=torch.float16,           #computations performed in half precision     
    bnb_4bit_use_double_quant=True,         #quantizes quantization constants for additional compression
)
```

**Output**

* Directory: `model-int4/`
* Precision: INT4 (NF4)
- Size: ~25% of FP16 model
---

## Stage 4: GGUF Conversion (FP16)

**Purpose**
Enable CPU inference using llama.cpp

**Process**:
1. Clone llama.cpp repository
2. Install Python requirements
3. Convert merged FP16 model to GGUF format using `convert_hf_to_gguf.py`
4. Build llama.cpp with CMake
5. Apply Q4_0 quantization using llama.cpp's quantization tool

**Command**

```bash
python llama.cpp/convert_hf_to_gguf.py \
  "/content/drive/MyDrive/Colab Notebooks/quantized/merged-fp16" \
  --outfile "/content/drive/MyDrive/Colab Notebooks/quantized/model-f16.gguf" \
  --outtype f16
```

**Output**

* `model-f16.gguf` 

**GGUF Format Benefits**:
- CPU-optimized inference
- Cross-platform compatibility
- Efficient memory mapping
- Support for various quantization schemes
- No Python runtime dependency
---

## Stage 5: GGUF Quantization (Q8_0 and Q4_0)

### Q8_0 Quantization

```bash
llama-quantize model-f16.gguf model-q8_0.gguf Q8_0
```

### Q4_0 Quantization

```bash
llama-quantize model-f16.gguf model-q4_0.gguf Q4_0
```

**Outputs**

* `model-q8_0.gguf`
* `model-q4_0.gguf`

**Q4_0 Characteristics**:
- 4-bit quantization optimized for llama.cpp
- Fastest CPU inference
- Smallest file size among GGUF variants
- Suitable for CPU-only deployments
---

## Model Size Measurement

Sizes are computed programmatically in the notebook using `os.path.getsize`.

Printed results:

```text
FP16 (merged-fp16/)        - 2102.13 MB
INT8 (model-int8/)         - 1179.66 MB
INT4 (model-int4/)         - 731.06 MB
GGUF-F16 (model-f16.gguf)  - 2099.05 MB
GGUF-Q8 (model-q8_0.gguf)  - 1115.62 MB
GGUF-Q4 (model-q4_0.gguf)  - 607.23 MB
```

---

## Summary of Formats

| Format     | Backend   | Precision | Target Use              |
| ---------- | --------- | --------- | ----------------------- |
| FP16       | HF        | 16-bit    | Training / High-end GPU |
| INT8       | HF        | 8-bit     | Mid-range GPU           |
| INT4 (NF4) | HF        | 4-bit     | Low-VRAM GPU            |
| GGUF-F16   | llama.cpp | 16-bit    | CPU / Hybrid            |
| GGUF-Q8_0  | llama.cpp | 8-bit     | Fast CPU inference      |
| GGUF-Q4_0  | llama.cpp | 4-bit     | Max compression CPU     |

---
