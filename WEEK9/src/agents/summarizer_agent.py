from autogen_agentchat.agents import AssistantAgent
#from autogen_ext.models.llama_cpp import LlamaCppChatCompletionClient
from autogen_ext.models.ollama import OllamaChatCompletionClient
#from autogen_core.model_context import BufferedChatCompletionContext

# model_client = LlamaCppChatCompletionClient(
#     model_path="/home/chandramohan/Desktop/Week1/WEEK9/src/models/qwen2.5-7b-instruct-q4_0.gguf",
#     n_ctx=2048
#     )
model_client = OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0")
summarizer_agent = AssistantAgent(
    name="SummarizerAgent",
    model_client=model_client,
    system_message="""You are a Summarizer Agent. Your job is to condense information.
    - Take raw research data
    - Create concise summaries in a paragraph
    - Do NOT provide final answers
    - Pass summaries to the Answer Agent""",
    #model_context=BufferedChatCompletionContext(buffer_size=10)
)