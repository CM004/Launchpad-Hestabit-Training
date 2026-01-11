
## SQL-QA Engine (LLM-Powered)
==============================

A small, schema-aware SQL Question-Answering engine that converts natural language 
questions into safe, read-only SQLite queries using an LLM (Gemini). It works on 
the Chinook database, blocks dangerous SQL, and returns short, human-friendly summaries.


## Architecture
----------------

User Question - plain text
        ↓
Schema Loader
        ↓
Prompt Construction - generate_sql(question, schema)
        ↓
LLM (Gemini)
        ↓
SQL Generation (Sql response)
        ↓
SQL Validation
        ↓
SQLite Execution - execute_sql(sql, db_path)
        ↓
Result Summarization - summarize_result(question, result(rows, columns)
        ↓
Final Answer


## Pipeline Steps
------------------

1. Schema extraction (schema_loader.py)
   - Reads table and column metadata from chinook.db
   - Gives the LLM an accurate schema so it does not invent tables/columns

2. Prompt construction (sql_generator.py)
   - Builds a prompt with:
       - Allowed tables and columns (schema) only
       - SQLite syntax rules
       - Hard rule: only SELECT queries, no comments or explanations, end with semicolon

3. SQL generation (LLM)
   - The LLM returns a SELECT ... query string for the user question
   - No extra explanation text is used in execution, only the SQL

4. SQL validation (sql_generator.py / pipeline)
   - Checks:
       - Query starts with SELECT
       - No INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE
   - If invalid → raises an error and stops

5. Safe execution (sql_pipeline.py)
   - Connects to SQLite using DB_PATH = "src/data/db/chinook.db"
   - Executes the validated SELECT query on db and fetches columns and rows

6. Result summarization (llm_client.py)
   - Asks the LLM for a short plain-English summary of the result
   - Used as the final user-facing answer


## Usage
---------
![alt text](<Screenshot from 2026-01-07 11-14-43.png>)


## Project Structure
---------------------

Day4/
  - src/
    - config/config.py             - API key + DB path
    - data/db/chinook.db           - SQLite database
    - utils/schema_loader.py       - Extract schema metadata
    - generator/llm_client.py      - Gemini API client
    - generator/sql_generator.py   - Generate & validate SQL
    - pipelines/sql_pipeline.py    - Main pipeline orchestrator
  - .env                           - GEMINI_API_KEY


## Security Features
-----------------

- Read-only queries: Only SELECT statements allowed
- SQL injection prevention: Validation before execution
- Forbidden operations: Blocks INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE
- Schema-aware prompts: LLM cannot hallucinate non-existent tables/columns
