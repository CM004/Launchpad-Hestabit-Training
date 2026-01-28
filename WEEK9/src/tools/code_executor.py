#import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
#from autogen_core.tools import FunctionTool

from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.code_executors.local  import LocalCommandLineCodeExecutor

executor = LocalCommandLineCodeExecutor()
# Create the Python code execution tool (no executor needed - it's built-in)
code_execution_tool = PythonCodeExecutionTool(executor=executor)
# model_client = LlamaCppChatCompletionClient(
#     model_path="/home/chandramohan/Desktop/Week1/WEEK9/src/models/qwen2.5-7b-instruct-q4_0.gguf",
#     n_ctx=2048)
code_agent = AssistantAgent(
    name = "CodeExecutorAgent",
    tools = [code_execution_tool],
    model_client = OllamaChatCompletionClient(model = "qwen2.5:7b-instruct-q4_0" ),
    system_message=(
        "You are a code execution agent. "
        "You receive data from previous steps in the Context section. "
        "Use io.StringIO to parse CSV data if provided. "
        "Example: import io, pandas as pd; df = pd.read_csv(io.StringIO(csv_data)) "
        "Always print clear results."
    ))

# task = """Write valid Python function code to write a linear search function.
# Use print keyword to print the output."""

# async def main():
#     result = await agent.run(task=task)
#     print(str(result.messages[-1].content))

# if __name__ == "__main__":
#     asyncio.run(main())
