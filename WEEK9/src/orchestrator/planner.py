import asyncio
from typing import List
from autogen_core import RoutedAgent, MessageContext, message_handler, AgentId
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
from orchestrator.messages import (
    UserTask,
    TaskPlan,
    WorkerTask, WorkerResult,
    ReflectionTask, ReflectionResult, 
    ValidationTask, ValidationResult, 
    FinalAnswer)

class PlannerAgent(RoutedAgent):
    
    def __init__(self,model_client: ChatCompletionClient,num_workers: int = 3,) -> None:
        super().__init__(description="Planner/Orchestrator Agent")
        self._model_client = model_client
        self._num_workers = num_workers
    
    @message_handler
    async def handle_task(self, message: UserTask, ctx: MessageContext) -> FinalAnswer:
        #Main orchestration logic - coordinates all agents. 
        print(f"\n{'#'*80} \nPLANNER/ORCHESTRATOR STARTED \nTask: {message.task} \n{'#'*80}\n")
        
        # === PHASE 1: PLANNING - Break task into subtasks ===
        task_plan = await self._plan_task(message.task)
        
        # === PHASE 2: WORKER EXECUTION (Layer 0 - Parallel) - Dispatch to parallel workers ===
        worker_results = await self._execute_workers(task_plan)
        
        # === PHASE 3: REFLECTION (Layer 1) - Synthesize worker outputs ===
        reflection_result = await self._execute_reflection(message.task, worker_results)
        
        # === PHASE 4: VALIDATION (Layer 2) - Check quality ===
        validation_result = await self._execute_validation(message.task, reflection_result.refined_result)
        
        # === PHASE 5: RETURN FINAL ANSWER and execution tree ===
        print(f"\n{'#'*80} \nORCHESTRATION COMPLETE \nValidation: {'PASS' if validation_result.is_valid else 'FAIL'} \n{'#'*80}\n")

        return FinalAnswer(
            result=validation_result.final_result,
            validation_status=validation_result.is_valid)
    
    async def _plan_task(self, task: str) -> TaskPlan:
        # Use LLM to break down task into subtasks (DAG generation).
        print(f"\n{'='*80} \nPHASE 1: TASK PLANNING \n{'='*80}")

        system_prompt = (
            "You are a Task Planner. Break down complex tasks into 3 independent subtasks.\n\n"
            "Rules:\n"
            "1. Each subtask should be self-contained and parallelizable\n"
            "2. Subtasks should cover different aspects of the main task\n"
            "3. Keep subtasks focused and specific\n\n"
            "Format your response as:\n"
            "SUBTASK_1: [description]\n"
            "SUBTASK_2: [description]\n"
            "SUBTASK_3: [description]\n")

        messages = [
            SystemMessage(content=system_prompt),
            UserMessage(content=f"Break down this task:\n{task}", source="user") ]
        
        model_result = await self._model_client.create(messages)

        # Parse subtasks from LLM output
        subtasks = self._parse_subtasks(str(model_result.content))
        
        # Create execution graph (DAG structure)
        execution_graph = {
            "layer_0": [f"subtask_{i}" for i in range(len(subtasks))],
            "layer_1": ["reflector"],
            "layer_2": ["validator"]}
        
        print(f"\nGenerated {len(subtasks)} subtasks:")
        for i, st in enumerate(subtasks):
            print(f"  {i+1}. {st[:80]}...")
        print(f"\nExecution Graph: {execution_graph}")
        print(f"{'='*80}\n")
        
        return TaskPlan(
            original_task=task,
            subtasks=subtasks,
            execution_graph=execution_graph)
    
    def _parse_subtasks(self, llm_output: str) -> List[str]:
        # Extract subtasks from LLM planning output.
        subtasks = []
        lines = llm_output.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('SUBTASK_'):
                # Extract after the colon
                if ':' in line:
                    subtask = line.split(':', 1)[1].strip()
                    subtasks.append(subtask)
        
        return subtasks[:self._num_workers]  # Limit to num_workers
    
    async def _execute_workers(self, task_plan: TaskPlan) -> List[WorkerResult]:
        print(f"\n{'='*80}  \nPHASE 2: PARALLEL WORKER EXECUTION  \n{'='*80}  \nDispatching {len(task_plan.subtasks)} workers...\n")
        
        # Create worker agent IDs
        worker_ids = [
            AgentId("worker", f"{self.id.key}/layer_0/worker_{i}")
            for i in range(len(task_plan.subtasks))]
        
        # Create worker tasks
        worker_tasks = [
            WorkerTask(
                task=subtask,
                subtask_id=f"subtask_{i}",
                previous_results=[]  # Layer 0 has no previous results
            )
            for i, subtask in enumerate(task_plan.subtasks)]
        
        print(f"\nDispatching {len(worker_tasks)} workers in parallel...")

        # Execute all workers in parallel using asyncio.gather
        results = await asyncio.gather(*[
            self.send_message(task, worker_id)
            for task, worker_id in zip(worker_tasks, worker_ids)])
        
        print(f"Received {len(results)} results\n{'='*80}\n")
        
        return results
    
    async def _execute_reflection(self, original_task: str, worker_results: List[WorkerResult]) -> ReflectionResult:
        print(f"\n{'='*80}  \nPHASE 3: REFLECTION & SYNTHESIS  \n{'='*80}  \nDispatching reflection...\n")
        
        reflection_id = AgentId("reflection", f"{self.id.key}/layer_1/reflection")
        reflection_task = ReflectionTask(
            original_task=original_task,
            worker_results=worker_results)
        
        print(f"\nDispatching reflection agent...")
        result = await self.send_message(reflection_task, reflection_id)
        
        print(f"Reflection complete\n{'='*80}\n")
        
        return result
    
    async def _execute_validation(self, original_task: str, reflected_result: str) -> ValidationResult:
        print(f"\n{'='*80}  \nPHASE 4: VALIDATION & QA  \n{'='*80}  \nDispatching validator...\n")
        
        validator_id = AgentId("validator", f"{self.id.key}/layer_2/validator")
        validation_task = ValidationTask(
            original_task=original_task,
            reflected_result=reflected_result)
        
        print(f"\nDispatching validator agent...")
        result = await self.send_message(validation_task, validator_id)
        
        print(f"Validation: {result.is_valid}\n{'='*80}\n")
        
        return result
