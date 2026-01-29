from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.model_context import BufferedChatCompletionContext

# model_client = LlamaCppChatCompletionClient(
#     model_path="/home/chandramohan/Desktop/Week1/WEEK9/src/models/qwen2.5-7b-instruct-q4_0.gguf",
#     n_ctx=2048
#     )
model_client = OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0")
research_agent = AssistantAgent(
    name="ResearchAgent",
    model_client=model_client,
    system_message="""You are a Research Agent. Your job is to gather and organize information.
    - Find relevant facts and data
    - Do NOT summarize or analyze
    - Only collect and present raw research information
    - Pass findings to the Summarizer Agent""",
    model_context=BufferedChatCompletionContext(buffer_size=10)
)