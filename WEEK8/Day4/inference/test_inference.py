import json
import asyncio
import time
import csv
import os
from openai import AsyncOpenAI
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_URL = "http://localhost:8080/v1"
MODEL_NAME = "model-q8_0.gguf"  #/home/chandramohan/Desktop/Week1/WEEK8/Day3/quantized/model-int4
RESULTS_FILE = "./benchmarks/results.csv"
PROMPTS_FILE = "inference/prompts.json"
BATCH_SIZE = 2

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def load_prompts(filepath):
    with open(filepath) as f:
        return json.load(f)


def calculate_accuracy(generated, expected):    # Calculate similarity between generated and expected answer using embeddings
    if not expected or not generated:
        return None
    
    embeddings = embedding_model.encode([generated, expected], normalize_embeddings=True) # Encode both texts to vectors
    gen_vec, exp_vec = embeddings
    
    dimension = gen_vec.shape[0]
    index = faiss.IndexFlatIP(dimension) # Use FAISS to compute cosine similarity
    index.add(np.array([exp_vec]))
    
    similarity, _ = index.search(np.array([gen_vec]), k=1)
    return float(similarity[0][0])


def save_to_csv(result):
    file_exists = os.path.exists(RESULTS_FILE)
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(result)

# Benchmark with Metrics
async def stream_single_prompt(client, prompt, expected, prompt_id, batch_id): # Process one prompt with streaming and collect metrics
    output = []
    token_count = 0
    start_time = time.time()
    first_token_time = None
    
    print(f"\nStarting Prompt {prompt_id} in Batch {batch_id}")
    print(f"Prompt: {prompt[:100]}...")
    
    try:
        stream = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.7,
            stream=True,
        )
        
        chunk_count = 0
        
        async for chunk in stream:  # Collect streaming tokens
            chunk_count += 1
            
            if not chunk.choices:
                continue  # Just skip
            
            delta = chunk.choices[0].delta
            if delta and delta.content:
                if first_token_time is None:
                    first_token_time = time.time()
                
                output.append(delta.content)
                token_count += len(delta.content.split())
                
                print(f"[Batch {batch_id} | Prompt {prompt_id}] {delta.content}", end="", flush=True)
        
        print(f"\nTotal chunks: {chunk_count}, Tokens: {token_count}")
        
    except Exception as e:
        print(f"\n[ERROR] Prompt {prompt_id} failed: {e}")
    
    end_time = time.time()
    print("\n" + "-" * 80)
    
    total_latency = end_time - start_time
    time_to_first_token = first_token_time - start_time if first_token_time else None
    tokens_per_second = token_count / total_latency if total_latency > 0 else 0
    
    full_response = "".join(output)
    accuracy = calculate_accuracy(full_response, expected)
    
    result = {
        "model": MODEL_NAME[-11:],
        "batch_id": batch_id,  # Add batch tracking
        "prompt_id": prompt_id,
        "prompt": prompt[:80] + "...",
        "tokens": token_count,
        "latency_sec": round(total_latency, 3),
        "ttft_sec": round(time_to_first_token, 3) if time_to_first_token else None,
        "tokens_per_sec": round(tokens_per_second, 2),
        "semantic_accuracy": round(accuracy, 4) if accuracy else None,
    }
    
    save_to_csv(result)
    return result

async def process_batch(client, prompts, batch_id):   #Process multiple prompts in parallel (batch inference)
    print(f"\nBatch {batch_id} " + "=" * 70 + "\n")
    
    tasks = []
    for idx, p in enumerate(prompts, start=1):
        task = stream_single_prompt(
            client,
            p["prompt"],
            p.get("output", ""),
            idx,
            batch_id
        )
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    print(f"\n[Batch {batch_id} Complete]\n")


def split_into_batches(data, batch_size): #Split list into smaller batches
    for i in range(0, len(data), batch_size):
        yield data[i : i + batch_size]


async def run_benchmark():
    # Initialize OpenAI client pointing to vLLM server
    client = AsyncOpenAI(base_url=BASE_URL, api_key="empty")
    all_prompts = load_prompts(PROMPTS_FILE)
    
    print(f"\n{'=' * 80}")
    print(f"Starting vLLM Benchmark")
    print(f"{'=' * 80}")
    print(f"Model: {MODEL_NAME}")
    print(f"Total prompts: {len(all_prompts)}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"{'=' * 80}\n")
    
    batch_num = 1
    for batch in split_into_batches(all_prompts, BATCH_SIZE):
        await process_batch(client, batch, batch_num)
        batch_num += 1
    
    print(f"\nBenchmark complete!")
    print(f"\nResults saved to: {RESULTS_FILE}\n")

# # Simple Streaming (one by one, no batching)
# async def simple_streaming(client, prompt):
#     """Stream one prompt at a time without batching"""
#     print(f"\nPrompt: {prompt[:80]}...")
#     print("Response: ", end="", flush=True)
    
#     stream = await client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=256,
#         temperature=0.7,
#         stream=True,
#     )
    
#     async for chunk in stream:
#         if not chunk.choices:
#             continue
        
#         delta = chunk.choices[0].delta
#         if delta and delta.content:
#             print(delta.content, end="", flush=True)
    
#     print("\n" + "-" * 60)

# # Batch Inference (buffer all, print after completion)
# async def batch_inference_buffered(client, prompt, prompt_id, batch_id):
#     """Process prompt and buffer output, print after completion"""
#     buffer = []
    
#     stream = await client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=256,
#         temperature=0.7,
#         stream=True,
#     )
    
#     async for chunk in stream:
#         if not chunk.choices:
#             continue
#         delta = chunk.choices[0].delta
#         if delta and delta.content:
#             buffer.append(delta.content)
    
#     # Print after completion
#     print(f"\nBatch {batch_id} | Prompt {prompt_id}: {prompt[:60]}...")
#     print("Response:")
#     print("".join(buffer))
#     print("-" * 80)


# async def run_batch_buffered(client, prompts, batch_id):
#     """Run batch with buffered output"""
#     print(f"\nBatch {batch_id} " + "=" * 70)
#     tasks = [
#         batch_inference_buffered(client, p["prompt"], i, batch_id)
#         for i, p in enumerate(prompts, start=1)
#     ]
#     await asyncio.gather(*tasks)


# # Real-time Parallel Streaming
# async def parallel_streaming(client, prompt, prompt_id, batch_id):
#     """Stream with real-time parallel output display"""
#     stream = await client.chat.completions.create(
#         model=MODEL_NAME,
#         messages=[{"role": "user", "content": prompt}],
#         max_tokens=256,
#         temperature=0.7,
#         stream=True,
#     )
    
#     async for chunk in stream:
#         if not chunk.choices:
#             continue
        
#         delta = chunk.choices[0].delta
#         if delta and delta.content:
#             # Show which prompt is generating in real-time
#             print(f"[B{batch_id}:P{prompt_id}] {delta.content}", flush=True)


# async def run_parallel_batch(client, prompts, batch_id):
#     """Run batch with live parallel streaming"""
#     print(f"\nBatch {batch_id} " + "=" * 70 + "\n")
#     tasks = [
#         parallel_streaming(client, p["prompt"], i, batch_id)
#         for i, p in enumerate(prompts, start=1)
#     ]
#     await asyncio.gather(*tasks)


# # to test individual implementations
# async def demo_simple_streaming():
#     """Demo: Simple streaming (Implementation 1)"""
#     client = AsyncOpenAI(base_url=BASE_URL, api_key="empty")
#     prompts = [p["prompt"] for p in load_prompts(PROMPTS_FILE)]
    
#     for prompt in prompts[:2]:  # Test first 2
#         await simple_streaming(client, prompt)


# async def demo_buffered_batch():
#     """Demo: Buffered batch inference (Implementation 2)"""
#     client = AsyncOpenAI(base_url=BASE_URL, api_key="empty")
#     prompts = load_prompts(PROMPTS_FILE)
    
#     for batch_id, batch in enumerate(split_into_batches(prompts, BATCH_SIZE), 1):
#         await run_batch_buffered(client, batch, batch_id)


# async def demo_parallel_streaming():
#     """Demo: Real-time parallel streaming (Implementation 3)"""
#     client = AsyncOpenAI(base_url=BASE_URL, api_key="empty")
#     prompts = load_prompts(PROMPTS_FILE)
    
#     for batch_id, batch in enumerate(split_into_batches(prompts, 4), 1):
#         await run_parallel_batch(client, batch, batch_id)


if __name__ == "__main__":
    asyncio.run(run_benchmark())                 # Run full benchmark 

    # asyncio.run(demo_simple_streaming())       # Test simple_streaming
    # asyncio.run(demo_buffered_batch())         # Test buffered_batch
    # asyncio.run(demo_parallel_streaming())     # Test parallel_streaming
