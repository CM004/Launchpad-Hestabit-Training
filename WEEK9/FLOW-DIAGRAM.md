# MOA System Flow Diagram

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUERY                              │
│              "Plan 4-day Mussoorie trip (₹15,000)"              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PLANNER AGENT                              │
│  - Receives UserTask                                            │
│  - Orchestrates entire workflow                                 │
│  - Returns FinalAnswer                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PHASE 1: PLANNING                            │
│  ┌───────────────────────────────────────────────────────┐      │
│  │ _plan_task()                                          │      │
│  │ - Calls LLM to decompose task                         │      │
│  │ - Generates 3 subtasks                                │      │
│  │ - Creates execution_graph (DAG)                       │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                 │
│  Output: TaskPlan with execution_graph:                         │
│  {                                                              │
│    "layer_0": ["subtask_0", "subtask_1", "subtask_2"],          │
│    "layer_1": ["reflector"],                                    │
│    "layer_2": ["validator"]                                     │
│  }                                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 2: PARALLEL WORKER EXECUTION                 │
│  ┌───────────────────────────────────────────────────────┐      │
│  │ _execute_workers()                                    │      │
│  │ - Creates 3 worker agents                             │      │
│  │ - Executes in parallel using asyncio.gather()         │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                 │
│     ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │
│     │  Worker 0    │   │  Worker 1    │   │  Worker 2    │      │
│     │ (Travel)     │   │ (Stay)       │   │ (Itinerary)  │      │
│     │              │   │              │   │              │      │
│     │ Uses LLM to  │   │ Uses LLM to  │   │ Uses LLM to  │      │
│     │ solve        │   │ solve        │   │ solve        │      │
│     │ subtask      │   │ subtask      │   │ subtask      │      │
│     └──────┬───────┘   └──────┬───────┘   └──────┬───────┘      │
│            │                  │                  │              │
│            └──────────────────┴──────────────────┘              │
│                             │                                   │
│  Output: List[WorkerResult]                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            PHASE 3: REFLECTION & SYNTHESIS                      │
│  ┌───────────────────────────────────────────────────────┐      │
│  │ _execute_reflection()                                 │      │
│  │ - Sends ReflectionTask to reflection agent            │      │
│  │ - Combines all worker results                         │      │
│  │ - LLM synthesizes coherent answer                     │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                 │
│     ┌────────────────────────────────────────────┐              │
│     │     REFLECTION AGENT                       │              │
│     │  - Receives worker_results                 │              │
│     │  - Uses LLM to merge & refine              │              │
│     │  - Returns refined_result                  │              │
│     └────────────────────────────────────────────┘              │
│                                                                 │
│  Output: ReflectionResult                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│               PHASE 4: VALIDATION & QA                          │
│  ┌───────────────────────────────────────────────────────┐      │
│  │ _execute_validation()                                 │      │
│  │ - Sends ValidationTask to validator agent             │      │
│  │ - Checks quality, correctness, completeness           │      │
│  └───────────────────────────────────────────────────────┘      │
│                                                                 │
│     ┌────────────────────────────────────────────┐              │
│     │     VALIDATOR AGENT                        │              │
│     │  - Receives reflected_result               │              │
│     │  - Uses LLM to validate                    │              │
│     │  - Returns is_valid + final_result         │              │
│     └────────────────────────────────────────────┘              │
│                                                                 │
│  Output: ValidationResult                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FINAL ANSWER                               │
│  FinalAnswer(                                                   │
│    result = validated_result,                                   │
│    validation_status = True/False                               │
│  )                                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## DAG Execution Structure

```
Layer 0 (Parallel)          Layer 1 (Serial)         Layer 2 (Serial)
==================          ================         ================

  subtask_0
     (W0)     ─┐
                ├─────────────►  reflector  ────────►  validator
  subtask_1     │                   (R)                    (V)
     (W1)     ─┤
                │
  subtask_2     │
     (W2)     ─┘

Dependencies:
- Layer 1 waits for ALL Layer 0 nodes
- Layer 2 waits for Layer 1 completion
- No cycles (Acyclic Graph)
```

---

## Agent Communication Flow

```
┌──────────────┐
│  Planner     │
│  (default)   │
└──────┬───────┘
       │ send_message(WorkerTask)
       ├─────────────────────────────────┐
       │                                 │
       ▼                                 ▼
┌──────────────┐                  ┌──────────────┐
│  Worker 0    │                  │  Worker 1    │
│  (layer_0/   │◄─ WorkerResult ─►│  (layer_0/   │
│   worker_0)  │                  │   worker_1)  │
└──────────────┘                  └──────────────┘
       │
       │ All results collected
       ▼
┌──────────────────────┐
│  Reflection Agent    │
│  (layer_1/           │
│   reflection)        │
└──────────┬───────────┘
           │ ReflectionResult
           ▼
┌──────────────────────┐
│  Validator Agent     │
│  (layer_2/           │
│   validator)         │
└──────────┬───────────┘
           │ ValidationResult
           ▼
     [Final Answer]
```

---

## Message Types

```
UserTask
  ├─ task: str

WorkerTask
  ├─ task: str
  ├─ subtask_id: str
  └─ previous_results: List[str]

WorkerResult
  └─ result: str

ReflectionTask
  ├─ original_task: str
  └─ worker_results: List[WorkerResult]

ReflectionResult
  └─ refined_result: str

ValidationTask
  ├─ original_task: str
  └─ reflected_result: str

ValidationResult
  ├─ is_valid: bool
  └─ final_result: str

FinalAnswer
  ├─ result: str
  └─ validation_status: bool
```

---

## Runtime Components

```
┌───────────────────────────────────────────────┐
│          SingleThreadedAgentRuntime           │
│                                               │
│  ┌─────────────────────────────────────┐      │
│  │     Agent Registry                  │      │
│  │    planner → PlannerAgent           │      │
│  │    worker → WorkerAgent             │      │
│  │    reflection → ReflectionAgent     │      │
│  │    validator → ValidatorAgent       │      │
│  └─────────────────────────────────────┘      │
│                                               │
│  ┌─────────────────────────────────────┐      │
│  │     Message Router                  │      │
│  │  Routes messages to correct agents  │      │
│  │  based on AgentId(type, key)        │      │
│  └─────────────────────────────────────┘      │
└───────────────────────────────────────────────┘
```

---

## Key Design Patterns

| Pattern | Implementation |
|---------|----------------|
| **Planner-Executor** | PlannerAgent orchestrates, Workers execute |
| **DAG Execution** | execution_graph defines layer dependencies |
| **Task Graph** | LLM generates subtasks → builds graph structure |
| **Agent Registry** | runtime.register(type, factory) pattern |
| **Parallel Execution** | asyncio.gather() for layer_0 workers |
| **Message Passing** | send_message(task, agent_id) for communication |

---

## Execution Timeline

```
T0 ─── Planner receives UserTask
T1 ─── LLM generates 3 subtasks
T2 ─── Create execution_graph
T3 ─── Dispatch 3 workers (parallel)
       │
       ├─ Worker 0 processing
       ├─ Worker 1 processing  
       └─ Worker 2 processing
       │
T4 ─── All workers complete
T5 ─── Reflection agent synthesizes
T6 ─── Validator checks quality
T7 ─── Return FinalAnswer
```