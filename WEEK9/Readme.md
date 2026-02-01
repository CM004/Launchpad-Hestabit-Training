# NEXUS AI

A production-ready autonomous multi-agent orchestration system that coordinates specialized AI agents with persistent memory capabilities.

***

## Features

- **8 Specialized Agents**: Planner, Researcher, Analyst, Coder, Critic, Optimizer, Validator, Reporter
- **Intelligent Planning**: Auto-decomposes complex tasks into 5-15 executable steps
- **Persistent Memory**: Remembers user preferences, past conversations, and learned facts
- **Context-Aware**: Uses FAISS semantic search to retrieve relevant information
- **Token-Optimized**: Prevents API overflow with automatic content truncation

***

## Project Structure

```
nexus_ai/
├── agents/
│   ├── planner_agent.py      # Task decomposition
│   ├── researcher_agent.py   # Information gathering
│   ├── analyst_agent.py      # Data analysis
│   ├── coder_agent.py        # Code generation
│   ├── critic_agent.py       # Quality review
│   ├── optimizer_agent.py    # Performance optimization
│   ├── validator_agent.py    # Result validation
│   ├── reporter_agent.py     # Report compilation
│   └── orchestrator.py       # Agent coordination
├── memory/
│   ├── agent_memory.py       # Memory system
│   ├── long_term.py          # SQLite persistence
│   ├── vector_store.py       # FAISS semantic search
│   └── session_memory.py     # Short-term memory
├── vectorstore/              # Auto-generated data
│   ├── agent_long_term.db
│   ├── agent_vectors.faiss
│   └── agent_vectors.meta
├── main.py                   # Entry point
├── .env                      # API key
└── requirements.txt          # Dependencies
```

***

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GROQ_API_KEY=gsk_..." > .env

# Run
python main.py
```

***

## Usage

### Basic Task Execution

```python
from agents.orchestrator import MemoryEnabledOrchestrator
from memory.agent_memory import AgentMemorySystem

# Initialize memory
memory = AgentMemorySystem(vector_threshold=0.3)

# Initialize orchestrator
orchestrator = MemoryEnabledOrchestrator(planner, agents, memory)

# Execute task
result = await orchestrator.execute("Plan a healthcare AI startup")
```

### Save Important Facts

```python
await orchestrator.save_important_fact(
    "User prefers Python for development",
    importance=9
)
```

### Memory Statistics

```python
stats = await orchestrator.get_memory_stats()
print(stats)

# Output:
# {
#   'session': {'size': 16},
#   'vector': {'size': 30},
#   'long_term': {
#     'total_memories': 45,
#     'episodic': 32,
#     'semantic': 13,
#     'avg_importance': 6.2
#   }
# }
```

***

## How It Works

```
1. User submits task
   ↓
   "Build a web scraper for product prices"

2. Planner decomposes
   ↓
   [Researcher → Coder → Validator → Reporter]

3. Memory retrieves
   ↓
   Relevant past work, user preferences

4. Agents execute
   ↓
   Each step with full context

5. Results saved
   ↓
   Long-term memory for future use
```

***

## Configuration

### Memory Settings

```python
memory = AgentMemorySystem(
    session_max_turns=50,      # Recent conversation history
    vector_k=5,                # Top-k similar memories
    vector_threshold=0.3,      # Similarity threshold (0-1)
    db_path="vectorstore/agent_long_term.db",
    vector_persist_path="vectorstore/agent_vectors.faiss"
)
```

***

## Requirements

- Python 3.12+
- autogen-agentchat==0.4.0
- autogen-ext[openai]==0.4.0
- faiss-cpu==1.7.4
- sentence-transformers==2.2.2
- python-dotenv==1.0.0

***

## Memory Layers

- **Session Memory**: Last 50 conversation turns (RAM)
- **Vector Store**: Semantic similarity search (FAISS, 384-dim)
- **Long-term DB**: Persistent facts and learnings (SQLite)

***

## Example Tasks

```python
# Research and analysis
await orchestrator.execute("Research RAG systems and create a report")

# Code generation
await orchestrator.execute("Build a sentiment analysis script")

# Multi-step workflow
await orchestrator.execute("Create a web app, optimize it, and document")

# Backend architecture
await orchestrator.execute("Design scalable backend for healthcare app")

# Memory-aware
await orchestrator.execute("What did we discuss last time?")
```

***

## Documentation

- **README.md** (this file): Quick start and usage
- **ARCHITECTURE.md**: Detailed system architecture
- **FINAL-REPORT.md**: Complete project report

