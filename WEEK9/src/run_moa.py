import asyncio
#import json
from autogen_core import SingleThreadedAgentRuntime, AgentId
from autogen_ext.models.ollama import OllamaChatCompletionClient
# Import agents
from orchestrator.messages import UserTask
from orchestrator.planner import PlannerAgent
from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectionAgent
from agents.validator import ValidatorAgent

async def main():  #Setup and run the multi-agent orchestration system.
    print("\n" + "="*80)
    print("MIXTURE OF AGENTS - MULTI-AGENT ORCHESTRATION")
    print("="*80 + "\n")

    model_client = OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0")
    print("Model loaded\n")                   # set up model client
    
    print("Setting up agent runtime...")
    runtime = SingleThreadedAgentRuntime()   # set up runtime
    # Register agent types with factory functions
    # Each registration creates an agent type that can spawn instances
    await WorkerAgent.register(  # Worker agents(multiple instances will be created dynamically)
        runtime,
        "worker",
        lambda: WorkerAgent(model_client=model_client))
    
    await ReflectionAgent.register(   # Reflection agent (single instance)
        runtime,
        "reflection",
        lambda: ReflectionAgent(model_client=model_client))
     
    await ValidatorAgent.register(   # Validator agent (single instance)
        runtime,
        "validator",
        lambda: ValidatorAgent(model_client=model_client))
    
    await PlannerAgent.register(   # Planner/Orchestrator agent (coordinates everything)
        runtime,
        "planner",
        lambda: PlannerAgent(model_client=model_client,num_workers=3))  # Number of parallel workers 
    
    print("Registered 4 agent types: planner, worker, reflection, validator\n")
    
    runtime.start()
    print("Runtime started\n")
    
    task = ("Plan a 4-day trip to Mussoorie within a ₹15,000 budget.Decompose the task into parallel steps (travel, stay, food, sightseeing), refine the itinerary, validate costs and feasibility, and present a final optimized plan.")
    print(f"User Task: {task}\n{'='*80}\n")

    result = await runtime.send_message( # === EXECUTE ORCHESTRATION ===
        UserTask(task=task),
        AgentId("planner", "default"))
        
    print("\n" + "="*80)
    print("FINAL RESULT")
    print("="*80 + "\n")
    print(result.result) # === DISPLAY RESULTS ===
    print("\n" + "="*80)
    print(f"Validation Status: {'PASS' if result.validation_status else 'FAIL'}")
    print("="*80 + "\n")
    
    await runtime.stop_when_idle()  # === CLEANUP ===
    print("Runtime stopped\n")

if __name__ == "__main__":
    asyncio.run(main())
