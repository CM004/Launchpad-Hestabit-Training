import sqlite3
import pandas as pd
import os 
#import asyncio
from typing_extensions import Annotated
from autogen_core.tools import FunctionTool
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient

if not os.path.exists('sales.csv'): 
    df = pd.DataFrame({
        'product': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard'],
        'sales': [150, 300, 200, 100, 400],
        'price': [50000, 30000, 20000, 15000, 2000]
    })
    df.to_csv('sales.csv', index=False)
    print("sales.csv created")

async def execute_sql(db_path: Annotated[str, "Database path"],query: Annotated[str, "SQL query"]) -> str:
     """Execute any SQL query (SELECT, INSERT, UPDATE, DELETE, CREATE)."""
     conn = sqlite3.connect(db_path)
    
    # Check if it's a SELECT query
     if query.strip().upper().startswith('SELECT'):
        df = pd.read_sql_query(query, conn)
        result = df.to_string()
     else:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        result = f"Query executed successfully. Rows affected: {cursor.rowcount}"
    
     conn.close()
     return result

async def csv_to_db(csv_path: Annotated[str, "CSV file path"],db_path: Annotated[str, "Database path"],table: Annotated[str, "Table name"]
) -> str:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    """Convert CSV to database."""
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql(table, conn, if_exists='replace', index=False)
    conn.close()
    return f"Created table '{table}' with {len(df)} rows"

sql_tool = FunctionTool(execute_sql, description="Run SQL queries")
csv_tool = FunctionTool(csv_to_db, description="Convert CSV to database")

db_agent = AssistantAgent(
    name="DBAgent",
    tools=[sql_tool, csv_tool],
    model_client=OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0")                                                                                                           ,
    system_message="You work with databases. Use tools to run any SQL queries including SELECT, INSERT, UPDATE, DELETE.")

# task = """
# DELETE products with sales less than 150 from sales.db table sales
# Then SELECT to show remaining products
# """

# async def main():
#     result = await agent.run(task=task)
#     print(result.messages[-1].content)

# if __name__ == "__main__":
#     asyncio.run(main())

