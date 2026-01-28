from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from autogen_core.model_context import BufferedChatCompletionContext

model_client = LlamaCppChatCompletionClient(
    model_path="/home/chandramohan/Desktop/Week1/WEEK9/src/models/qwen2.5-7b-instruct-q4_0.gguf",
    n_ctx=2048
    )

answer_agent = AssistantAgent(
    name="AnswerAgent",
    model_client=model_client,
    system_message="""You are an Answer Agent. Your job is to provide final answers.
    - Take summarized information
    - Formulate clear, direct answers
    - Provide final actionable responses
    - This is the final step in the pipeline""",
    model_context=BufferedChatCompletionContext(buffer_size=10)
)
