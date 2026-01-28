from autogen_core import RoutedAgent, MessageContext, message_handler
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
from orchestrator.messages import ReflectionTask, ReflectionResult

class ReflectionAgent(RoutedAgent):
#Reflection agent that synthesizes multiple worker results and improves the quality through critical evaluation.
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(description="Reflection Agent - Quality Improvement")
        self._model_client = model_client
    
    @message_handler
    async def handle_task(self, message: ReflectionTask, ctx: MessageContext) -> ReflectionResult:
        combined = "\n\n".join([
            f"Worker {i+1} (Agent: {wr.agent_id}, Subtask: {wr.subtask_id}):\n{wr.result}"
            for i, wr in enumerate(message.worker_results)])
        
        prompt = (
            "You are a Reflection Agent."
            "Analyze multiple worker outputs and synthesize a improved superior answer."
            "Identify contradictions, gaps, and combine best insights. "
            "Ensure logical consistency and completeness.\n\n"
            "Worker outputs:\n" + combined)
        
        messages = [
        SystemMessage(content=prompt),
        UserMessage(content=f"Original task: {message.original_task}\n\nSynthesize the outputs.", source="user")]
        
        model_result = await self._model_client.create(messages)
        
        result_text = str(model_result.content)
        print(f"\n{'='*80}\nReflection-{self.id.key}\n{'-'*80}\n{result_text[:300]}...\n{'='*80}\n")
        
        return ReflectionResult(
        refined_result=result_text)
# from autogen_core import RoutedAgent, MessageContext, message_handler
# from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
# from orchestrator.messages import ReflectionTask, ReflectionResult

# class ReflectionAgent(RoutedAgent):    
#     def __init__(self, model_client: ChatCompletionClient) -> None:
#         super().__init__(description="Reflection Agent - Quality Improvement")
#         self._model_client = model_client
    
#     @message_handler
#     async def handle_task(self, message: ReflectionTask, ctx: MessageContext) -> ReflectionResult:

#         # Build comprehensive context from all worker results
#         system_prompt = (
#             "You are a Reflection Agent specialized in critical analysis and synthesis.\n\n"
#             "Your responsibilities:\n"
#             "1. Analyze multiple worker outputs for the same task\n"
#             "2. Identify strengths, weaknesses, contradictions, and gaps\n"
#             "3. Synthesize a superior answer that combines the best insights\n"
#             "4. Ensure logical consistency, accuracy, and completeness\n"
#             "5. Document what improvements you made\n\n"
#             "Worker outputs to analyze:\n")
        
#         # Add each worker result with clear separation
#         for i, worker_result in enumerate(message.worker_results):
#             system_prompt += (
#                 f"\n--- Worker {i+1} (Agent: {worker_result.agent_id}, "
#                 f"Subtask: {worker_result.subtask_id}) ---\n"
#                 f"{worker_result.result}\n")
        
#         system_prompt += (
#             "\n\nProvide your refined answer followed by a section explaining "
#             "what improvements you made.")
        
#         messages = [
#             SystemMessage(content=system_prompt),
#             UserMessage(
#                 content=f"Original task: {message.original_task}\n\n"
#                         f"Synthesize and improve the worker outputs above.",
#                 source="user")]
        
#         # Execute with local Qwen model
#         model_result = await self._model_client.create(messages)
#         assert isinstance(model_result.content, str)
        
#         # Parse response to extract improvements (simple split)
#         result_text = model_result.content
#         if "improvements:" in result_text.lower():
#             parts = result_text.lower().split("improvements:")
#             refined = parts[0].strip()
#             improvements = parts[1].strip() if len(parts) > 1 else "Enhanced synthesis"
#         else:
#             refined = result_text
#             improvements = "Synthesized multiple perspectives into coherent answer"
        
#         # Log output
#         print(f"\n{'='*80}")
#         print(f"Reflection-{self.id.key}")
#         print(f"{'-'*80}")
#         print(f"Refined Result:\n{refined[:300]}...")
#         print(f"\nImprovements Made:\n{improvements[:200]}...")
#         print(f"{'='*80}\n")
        
#         return ReflectionResult(
#             refined_result=refined,
#             improvements_made=improvements
#         )
