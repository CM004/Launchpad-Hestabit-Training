import os
import pandas as pd
#import asyncio
from typing_extensions import Annotated
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient

# Only create output.txt 
if not os.path.exists('output.txt'):
    with open('output.txt', 'w') as f:
        f.write('This is a sample text file.\nIt has multiple lines.')
    print("output.txt created")

async def read_file(file_path: Annotated[str, "Path to file"]) -> str:
    """Read CSV or text file."""
    if file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            csv_content = f.read()
        return csv_content  # Return raw CSV, not formatted string
    else:
        with open(file_path, 'r') as f:
            content = f.read()
        return content

async def write_file(
    file_path: Annotated[str, "Path to file"],
    content: Annotated[str, "Content to write"]
) -> str:
    """Write content to text file."""
    with open(file_path, 'w') as f:
        f.write(content)
    return f"Successfully wrote to {file_path}"

read_tool = FunctionTool(read_file, description="Read text or CSV file")
write_tool = FunctionTool(write_file, description="Write content from CSV file to text file")

file_agent = AssistantAgent(
    name="FileAgent",
    tools=[read_tool, write_tool],
    model_client=OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0"),
    system_message=(
        "You are a file processing agent. "
        "You MUST complete all steps in the task. "
        "After reading a file, you MUST write the output to the requested file."
    )
)

# async def main():
#     # Step 1: Read data
#     print("Reading sales.csv...")
#     result1 = await agent.run(task='Read sales.csv using read_file tool')
#     # data = result1.messages[-2].content[0].content  # Get tool result
#     # print(f"Data received:\n{data}\n")
    
#     # Step 2: Write data
#     print("Writing summary...")
#     result2 = await agent.run(
#         task=f"""
#         Step 1: First, read sales.csv using read_file tool 
#         Step 2:  Write a summary to output.txt using write_file tool in your own words.
#         """
#     )
    
#     print("Task finished. Check output.txt")
#     # with open('output.txt', 'r') as f:
#     #     print(f.read())

# if __name__ == "__main__":
#     asyncio.run(main())
