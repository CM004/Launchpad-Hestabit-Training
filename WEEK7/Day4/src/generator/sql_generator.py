import os
import sys
sys.path.append('src')

import re
from generator.llm_client import generate_answer

def generate_sql(question, schema):
    prompt = f"""Database Schema:
{schema}

Question: {question}

Generate ONLY a SELECT SQL query using SQLite syntax. End with semicolon.

SQL:"""
    
    response = generate_answer(prompt)
    
    # Extract SQL
    match = re.search(r'SELECT[\s\S]*?;', response, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    
    return response.replace("```sql", "").replace("```", "").strip()

def validate_sql(sql):
    forbidden = ["drop", "delete", "insert", "update", "alter", "truncate"]
    lowered = sql.lower()
    
    if not lowered.strip().startswith("select"):
        raise ValueError("Only SELECT queries allowed")
    
    for word in forbidden:
        if word in lowered:
            raise ValueError(f"{word} query not allowed")
