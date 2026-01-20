# FINAL REPORT – Quantised LLM Capstone Project

## 1. Project Overview

This capstone project focuses on building a **Quantised LLM inference system** with:

* A FastAPI backend
* Streaming responses by default
* A simple Streamlit-based chat UI
* Clean separation of configuration, model loading, API layer, and UI

---

## 2. System Architecture

### High-Level Architecture

```
[ Streamlit UI ]
        |
        |  HTTP (Streaming)
        v
[ FastAPI Backend ]
        |
        |  OpenAI-compatible client (base_url=http://localhost:8080/v1)
        v
[ Quantised LLM server (llama.cpp on port 8080) ]

```
---

## 3. Backend Design

### 3.1 Technology Stack

* **FastAPI** – API framework
* **OpenAI-compatible client** – Unified interface for local / remote models
* **Quantised LLM (TinyLlama-1.1B-Chat-v1.0 - Q8_0 GGUF)** – Efficient inference
* **Python generators** – Token streaming
---

### 3.2 Model Serving

* The model is **served independently** using `llama.cpp server` on port 8080
* FastAPI connects to the pre-running server using OpenAI-compatible client
* Decouples model inference from application logic
* Eliminates repeated loading overhead across requests

```text
llama.cpp server (port 8080) ← FastAPI connects (BASE_URL) → Ready to handle requests


```

---

### 3.3 API Endpoints

#### `/generate`

* Stateless, single-turn inference
* Always streams output
* No server-side memory

#### `/chat`

* Stateful, multi-turn conversation
* Maintains chat history using `chat_id`

---

### 3.4 Streaming Implementation

* Streaming is **always enabled by default**
* Uses:

  * `stream=True` from the OpenAI-compatible client
  * `StreamingResponse` from FastAPI

This ensures:

* Low latency
* Progressive output
* Better UX for long responses

---

## 4. Frontend (UI) Design

### 4.1 Technology Stack

* **Streamlit** – Rapid UI development
* **requests (streaming)** – HTTP streaming support

---

### 4.2 UI Features

* Chat-style interface (`st.markdown`) for displaying messages
* Sidebar controls:

  * Temperature
  * Top-p
  * Top-k
  * Max tokens
  * Clear chat button
* Mode switch:

  * Chat (stateful)
  * Generate (stateless)

---