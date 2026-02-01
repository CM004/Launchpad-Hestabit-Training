from autogen_core.memory import Memory, MemoryContent, MemoryMimeType, MemoryQueryResult, UpdateContextResult
# import asyncio
#from autogen_agentchat.agents import AssistantAgent
#from autogen_ext.models.ollama import OllamaChatCompletionClient

class SessionMemory(Memory):
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.turns = []
    
    async def add(self, content: MemoryContent):
        """Store conversation turn"""
        self.turns.append(content.content)
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)
    
    async def query(self, query: str) -> MemoryQueryResult:
        """Return all all messages wrapped in MemoryContent"""
        memory_contents = [
            MemoryContent(content=text, mime_type=MemoryMimeType.TEXT)
            for text in self.turns
        ]
        # Wrap in MemoryQueryResult (required by AutoGen)
        return MemoryQueryResult(results=memory_contents)
    
    async def update_context(self, model_context) -> UpdateContextResult:
        """Inject memories into agent context"""
        # Get all memories
        query_result = await self.query("")

        # Return them wrapped in UpdateContextResult
        return UpdateContextResult(memories=query_result)
    
    async def clear(self):
        self.turns = []
    
    async def close(self):
        pass

    def __len__(self):
        """Get number of stored messages"""
        return len(self.turns)

# async def main():
#     # Create memory (keeps last 5 messages)
#     memory = SessionMemory(max_turns=5)
    
#     # Create agent with memory
#     agent = AssistantAgent(
#         name="Agent",
#         model_client=OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0"),
#         memory=[memory],
#         system_message="You are a helpful assistant."
#     )
    
#     while True:
#         user_input = input("\nYou: ").strip()
        
#         if user_input == 'quit':
#             print("Goodbye!")
#             break
        
#         if user_input == 'debug':
#             result = await memory.query("")
#             print(f"Stored messages: {len(result.results)}")
#             for msg in result.results:
#                 print(f" {msg.content[:60]}")
#             continue
        
#         if user_input == 'clear':
#             await memory.clear()
#             print("Memory cleared.")
#             continue
        
#         if not user_input:
#             continue
        
#         # Get response from agent
#         result = await agent.run(task=user_input)
#         response = result.messages[-1].content
#         print(f"Agent: {response}")

#         await memory.add(MemoryContent(content=f"User: {user_input}", mime_type=MemoryMimeType.TEXT))
#         await memory.add(MemoryContent(content=f"Assistant: {response}", mime_type=MemoryMimeType.TEXT))

# if __name__ == "__main__":
#     asyncio.run(main())