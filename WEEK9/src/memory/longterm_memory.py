import sqlite3
from datetime import datetime
from autogen_core.memory import Memory,MemoryContent,MemoryMimeType,MemoryQueryResult,UpdateContextResult
from autogen_core.models import UserMessage

class LongTermMemory(Memory):
    def __init__(self, db_path: str = "memory/long_term.db"):
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance INTEGER DEFAULT 5,
                timestamp TEXT NOT NULL
            )""")
        conn.commit()
        conn.close()
    
    async def add(self, content: MemoryContent, memory_type: str = "episodic", importance: int = 5):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO memories (content, memory_type, importance, timestamp) VALUES (?, ?, ?, ?)",
            (content.content, memory_type, importance, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
    
    async def query(self, query: str = "", memory_type: str = None, limit: int = 20) -> MemoryQueryResult:
        conn = sqlite3.connect(self.db_path)
        
        if memory_type:
            cursor = conn.execute(
                "SELECT content FROM memories WHERE memory_type = ? ORDER BY importance DESC, timestamp DESC LIMIT ?",
                (memory_type, limit)
            )
        else:
            cursor = conn.execute(
                "SELECT content FROM memories ORDER BY importance DESC, timestamp DESC LIMIT ?",
                (limit,)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        memory_contents = [
            MemoryContent(content=row[0], mime_type=MemoryMimeType.TEXT)
            for row in rows
        ]
        
        return MemoryQueryResult(results=memory_contents)
    
    async def update_context(self, model_context) -> UpdateContextResult:
        query_result = await self.query(memory_type="semantic", limit=10)

        if query_result.results:
            for i,mem in enumerate (query_result.results, 1):
                memory_text = f" User Info:\n {i}. {mem.content}"
                await model_context.add_message(
                    UserMessage(content=memory_text, source = "memory")
                )
        return UpdateContextResult(memories=query_result)
    
    async def clear(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM memories")
        conn.commit()
        conn.close()
    
    async def close(self):
        pass
    
    def count(self, memory_type: str = None) -> int:
        conn = sqlite3.connect(self.db_path)
        if memory_type:
            cursor = conn.execute("SELECT COUNT(*) FROM memories WHERE memory_type = ?", (memory_type,))
        else:
            cursor = conn.execute("SELECT COUNT(*) FROM memories")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_all_semantic_facts(self):
        """Get all user facts (for loading into deduplication tracker)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT content FROM memories WHERE memory_type = 'semantic'")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
