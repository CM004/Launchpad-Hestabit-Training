# NEXUS AI - System Architecture

## Overview

Autonomous multi-agent orchestration system with persistent memory, built on AutoGen framework and Groq LLM infrastructure.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│                          (main.py)                           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR LAYER                        │
│              (MemoryEnabledOrchestrator)                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Memory Context Builder                              │   │
│  │  - Retrieves important facts (importance >= 7)       │   │
│  │  - Queries vector store (top-k semantic search)      │   │
│  │  - Fetches recent session (last 2 turns)            │   │
│  │  - Truncates content to prevent token overflow       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      PLANNING LAYER                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  PlannerAgent                                        │   │
│  │  - Decomposes task into ordered steps               │   │
│  │  - Assigns steps to specialized agents              │   │
│  │  - Outputs strict JSON execution plan               │   │
│  │  - Considers full memory context                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION LAYER                           │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │Researcher│ Analyst  │  Coder   │ Critic   │Optimizer│   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
│  ┌──────────┬──────────┐                                     │
│  │Validator │ Reporter │                                     │
│  └──────────┴──────────┘                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      MEMORY LAYER                            │
│                   (AgentMemorySystem)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Session Memory (RAM)                                │   │
│  │  - Last 50 conversation turns                        │   │
│  │  - Temporary context window                          │   │
│  │  - Cleared on restart                                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Vector Store (FAISS)                                │   │
│  │  - Semantic embeddings via all-MiniLM-L6-v2         │   │
│  │  - Similarity search (cosine via L2 normalized)      │   │
│  │  - 384-dim vectors, top-k=5, threshold=0.3          │   │
│  │  - Persisted: vector_store.faiss + .meta            │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Long-term Memory (SQLite)                           │   │
│  │  - Persistent storage with importance scoring        │   │
│  │  - Type classification (semantic/episodic)           │   │
│  │  - Indexed queries on importance and type            │   │
│  │  - File: agent_long_term.db                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Orchestrator

**File**: `agents/orchestrator.py`

**Class**: `MemoryEnabledOrchestrator`

**Responsibilities**:
- Coordinate workflow execution across multiple agents
- Build comprehensive memory context for planning
- Manage agent communication and result aggregation
- Save execution results to persistent memory
- Handle content truncation to prevent token overflow

**Key Methods**:
```python
execute(user_goal, use_memory=True)
_build_comprehensive_memory_context(query)
_build_agent_context(task, previous_results, ...)
_save_to_memory(content, importance, memory_type)
_truncate_content(content, max_length)
_parse_plan(plan_response)
_compile_results(results)
```

### 2. Planner Agent

**File**: `agents/planner_agent.py`

**Purpose**: Task decomposition and agent assignment

**Input**: User goal + Memory context

**Output**: JSON execution plan
```json
{
  "steps": [
    {"agent": "Researcher", "task": "Research healthcare AI market 2026"},
    {"agent": "Analyst", "task": "Analyze competitor landscape and gaps"},
    {"agent": "Coder", "task": "Design MVP feature set and architecture"},
    {"agent": "Critic", "task": "Review feasibility and compliance"},
    {"agent": "Reporter", "task": "Compile final startup plan"}
  ]
}
```

### 3. Execution Agents

| Agent | Role | Output |
|-------|------|--------|
| **Researcher** | Information gathering | Research findings, documentation, best practices |
| **Analyst** | Data analysis, trade-off evaluation | Insights, patterns, risk assessment |
| **Coder** | Code generation | Clean, commented, working code |
| **Critic** | Quality review, issue identification | Problems, flaws, improvement suggestions |
| **Optimizer** | Performance tuning | Optimizations, efficiency improvements |
| **Validator** | Correctness verification | Validation report, pass/fail status |
| **Reporter** | Result compilation | Structured final report |

### 4. Memory System

**File**: `memory/agent_memory.py`

**Class**: `AgentMemorySystem`

**Components**:

#### Session Memory
- **Storage**: In-memory list
- **Capacity**: 50 turns (configurable)
- **Use**: Recent conversation context
- **Persistence**: No (clears on restart)
- **File**: `session_memory.py`

#### Vector Store
- **Backend**: FAISS (IndexFlatL2)
- **Model**: all-MiniLM-L6-v2 (384-dim)
- **Similarity**: Cosine (L2 normalized)
- **Configuration**: k=5, threshold=0.3
- **Use**: Semantic search for relevant memories
- **Persistence**: Yes (saved to disk)
- **Files**: `agent_vectors.faiss`, `agent_vectors.meta`
- **Source**: `vector_store.py`

#### Long-term Memory
- **Backend**: SQLite
- **Schema**:
  ```sql
  CREATE TABLE memories (
    id INTEGER PRIMARY KEY,
    content TEXT,
    memory_type TEXT,      -- 'semantic' or 'episodic'
    mime_type TEXT,
    metadata TEXT,
    importance INTEGER,     -- 0-10 score
    created_at TIMESTAMP
  );
  CREATE INDEX idx_memory_type ON memories(memory_type);
  CREATE INDEX idx_importance ON memories(importance DESC);
  ```
- **Use**: Persistent facts and important information
- **Persistence**: Yes
- **File**: `agent_long_term.db`
- **Source**: `long_term.py`

## Data Flow

### Task Execution Flow

```
1. User Input
   ↓
2. Orchestrator receives task
   ↓
3. Query memory for relevant context
   - Long-term: get_important_memories(importance >= 7, limit=3)
   - Vector: query(user_goal, k=2)
   - Session: get_recent(n=2)
   ↓
4. Build memory context (formatted sections with truncation)
   ↓
5. Planner creates execution plan
   ↓
6. Save user goal to memory (importance=6, episodic)
   ↓
7. For each step:
   a. Build agent context (memory + task + previous, all truncated)
   b. Execute agent
   c. Save result to memory (importance=6, episodic) if key agent
   ↓
8. Compile final result (last agent output)
   ↓
9. Save to long-term (importance=7, semantic)
   ↓
10. Return to user
```

### Memory Save Flow

```
Content → Truncate to max_length
           ↓
        MemoryContent object
        (content, mime_type, metadata)
           ↓
        AgentMemorySystem.add(store_long_term=True)
           ↓
    ┌──────┴──────┬──────────┬──────────┐
    ↓             ↓          ↓          ↓
Session.add()  Vector.add()  LongTerm.add()
    │             │              │
    ↓             ↓              ↓
  RAM List    FAISS Index    SQLite DB
              + Pickle       (indexed)
```

### Memory Retrieval Flow

```
Query String
    ↓
AgentMemorySystem.get_context_for_query()
    ↓
┌───────┴────────┬──────────────┬─────────────┐
↓                ↓              ↓             ↓
Session       Vector        Long-term
get_recent(5)  query(k=5)    get_important(7, 5)
    ↓            ↓              ↓
Last 5 turns  Semantic search  Important facts
    ↓            ↓              ↓
Combined & Deduplicated (by content)
    ↓
Formatted Context
    ↓
Agent Prompt
```

## Memory Context Format

Agents receive context in structured sections:

```
=== IMPORTANT INFORMATION ===
 • User's name is Chandramohan
 • User is based in India
 • User prefers Python for development

=== RELEVANT PAST CONTEXT ===
 • Previously discussed healthcare AI startups
 • Built scalable backend architecture last session

=== RECENT CONVERSATION ===
 • User asked: Plan a startup in AI for healthcare
 • System created 5-step execution plan

=== RELEVANT TO THIS TASK ===
 • Healthcare AI market size projected at $10B
 • Key competitors: X, Y, Z with focus on diagnostics

=== ORIGINAL GOAL ===
Plan a startup in AI for healthcare

=== YOUR TASK ===
Research updated market, competitor, and trend analysis for AI in healthcare (2026+)

=== PREVIOUS STEPS ===
 • Reporter: Collected all previous outputs: summary of discussions...
 • Analyst: Identified missing components: regulatory compliance...
```

**Truncation Limits**:
- Memory context: 400 chars
- Task memories: 100 chars each
- Original goal: 150 chars
- Current task: 250 chars
- Previous outputs: 150 chars each (last 1 only)