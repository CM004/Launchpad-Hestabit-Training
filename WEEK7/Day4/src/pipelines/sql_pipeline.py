import os
import sys
sys.path.append('src')

import sqlite3
from config.config import DB_PATH
from utils.schema_loader import load_schema
from generator.sql_generator import generate_sql, validate_sql
from generator.llm_client import generate_answer

def execute_sql(sql, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return columns, rows

def summarize_result(question, columns, rows):
    if not rows:
        return "No results found."
    
    table = "\n".join(
        [" | ".join(columns)] +
        [" | ".join(map(str, r)) for r in rows[:5]]
    )
    
    prompt = f"Question: {question}\n\nResults:\n{table}\n\nSummarize in plain English:"
    return generate_answer(prompt)

def run_sql_qa(question):
    # Load schema
    schema = load_schema(DB_PATH)
    
    # Generate SQL
    sql = generate_sql(question, schema)
    print(f"\nGenerated SQL: {sql}")
    
    # Validate SQL
    validate_sql(sql)
    
    # Execute SQL
    columns, rows = execute_sql(sql, DB_PATH)
    
    # Summarize result
    answer = summarize_result(question, columns, rows)
    
    return answer

if __name__ == "__main__":
    print("\n=== SQL Question Answering System ===\n")
    
    while True:
        question = input("\nAsk a question (or 'exit' to quit): ")
        
        if question.lower() in ['exit', 'quit', 'q']:
            print("Bye bye!")
            break
        
        if not question.strip():
            continue
        
        try:
            answer = run_sql_qa(question)
            print(f"\nAnswer: {answer}\n")
            print("-" * 60)
        except Exception as e:
            print(f"Error: {e}")

