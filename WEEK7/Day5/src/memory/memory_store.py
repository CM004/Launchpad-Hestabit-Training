import json
from datetime import datetime
from pathlib import Path

class MemoryStore:
    def __init__(self):
        self.sessions = {}
        self.log_file = Path("src/logs/CHAT-LOGS.json")
        self.log_file.parent.mkdir(exist_ok=True)
    
    def add(self, sid, role, text):
        if sid not in self.sessions:
            self.sessions[sid] = []
        
        msg = {"role": role, "text": text, "time": datetime.now().isoformat()}
        self.sessions[sid].append(msg)
        
        if len(self.sessions[sid]) > 5: #keep last 5 only
            self.sessions[sid] = self.sessions[sid][-5:]
        
        print(f"[{msg['time']}] {sid} | {role}: {text[:50]}...")
        self.save()
        return msg
    
    def get(self, sid):
        return self.sessions.get(sid, [])
    
    def save(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)

mem = MemoryStore()
