import sqlite3

def load_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    schema = []
    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        col_desc = ", ".join(f"{col[1]} ({col[2]})" for col in columns)
        schema.append(f"Table {table}: {col_desc}")
    
    conn.close()
    return "\n".join(schema)
