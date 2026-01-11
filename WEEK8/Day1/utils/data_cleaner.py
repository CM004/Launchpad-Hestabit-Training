import json
import tiktoken
import matplotlib.pyplot as plt
import os

INPUT_PATH = "data/raw/coding_raw_2000.jsonl"
OUTPUT_TRAIN = "data/train.jsonl"
OUTPUT_VAL = "data/val.jsonl"
OUTPUT_DIR = "analysis"
MAX_TOKENS = 2000

os.makedirs(os.path.dirname(OUTPUT_TRAIN), exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    if not text:
        return 0
    return len(encoding.encode(text))

# Load all samples
samples = []
with open(INPUT_PATH, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            samples.append(json.loads(line))
        except:
            continue

print(f"Loaded {len(samples)} samples")

# Analyze tokens and clean
lengths = []
clean_samples = []

for s in samples:
    instruction = s.get("instruction", "")
    input_text = s.get("input", "")
    output = s.get("output", "")
    
    instr_len = count_tokens(instruction)
    input_len = count_tokens(input_text)
    output_len = count_tokens(output)
    total_len = instr_len + input_len + output_len
    
    lengths.append(total_len)
    
    if (total_len <= MAX_TOKENS and 
        instr_len > 0 and 
        output_len > 0):
        clean_samples.append(s)

print(f"Cleaned samples: {len(clean_samples)}")

# Split 80/20
split_idx = int(0.8 * len(clean_samples))
train, val = clean_samples[:split_idx], clean_samples[split_idx:]

with open(OUTPUT_TRAIN, "w") as f:
    for item in train:
        f.write(json.dumps(item) + "\n")

with open(OUTPUT_VAL, "w") as f:
    for item in val:
        f.write(json.dumps(item) + "\n")

# Token analysis
print(f"Total samples: {len(samples)}")
print(f"Train: {len(train)} | Val: {len(val)}")
print(f"Avg tokens: {sum(lengths)/len(lengths):.2f}")
print(f"Max: {max(lengths)} | Min: {min(lengths)}")

# Plot distribution
plt.figure(figsize=(10, 6))
plt.hist(lengths, bins=50, color='skyblue', edgecolor='black')
plt.xlabel("Token Length")
plt.ylabel("Frequency")
plt.title("Token Distribution - CS Dataset")
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, "token_distribution.png"), dpi=300)
print(f"Plot saved to: {OUTPUT_DIR}/token_distribution.png")