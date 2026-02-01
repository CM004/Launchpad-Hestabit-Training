import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.memory import MemoryContent, MemoryMimeType
from unified_memory import UnifiedMemory
from fact_extractor import extract_facts, existing_user_facts

async def main():
    os.makedirs("db", exist_ok=True)
    os.makedirs("memory", exist_ok=True)
    
    # Create memory and agent
    memory = UnifiedMemory()
    
    existing_facts = memory.longterm.get_all_semantic_facts()
    for fact in existing_facts:
        existing_user_facts.add(fact.lower().replace(' ', ''))
    
    agent = AssistantAgent(
        name="Agent",
        model_client=OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0"),
        memory=[memory],
        system_message="You are a helpful assistant with memory." )
    
    print(f"Loaded: {len(existing_facts)} facts, {len(memory.vector)} embeddings")
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input == 'quit':
            await memory.close()
            print("Goodbye!")
            break
        
        if user_input == 'debug':
            session_result = await memory.session.query("")
            user_facts = await memory.longterm.query(memory_type="semantic", limit=10)
            context = await memory.longterm.query(memory_type="episodic", limit=10)
            
            print(f"\nCurrent Session Messages = {len(session_result.results)}:")
            for i, mem in enumerate(session_result.results, 1):
                print(f"  {i}. {mem.content[:60]}")
            print(f"\nUser Facts = {len(user_facts.results)}:")
            for i, fact in enumerate(user_facts.results, 1):
                print(f"  {i}. {fact.content}")
            print(f"\nContext = {len(context.results)}:")
            for i, fact in enumerate(context.results, 1):
                print(f"  {i}. {fact.content}")
            continue
        
        if user_input.startswith('search '):
            results = await memory.query(user_input[7:])
            print(f"\nFound {len(results.results)} memories:")
            for i, mem in enumerate(results.results, 1):
                sim = mem.metadata.get('similarity', 0) if mem.metadata else 0
                print(f"  {i}.{mem.content}, similarity score = {sim:.2f}")
            continue
        
        if user_input == 'clear':
            await memory.clear()
            existing_user_facts.clear()
            print("All memories cleared")
            continue
        
        if not user_input:
            continue
        
        # Main flow: Search → Inject → Generate → Store
        results = await memory.query(user_input)
        
        enhanced_task = user_input
        if results.results:
            context = "Relevant memories:\n"
            for i, mem in enumerate(results.results[:2], 1):
                sim = mem.metadata.get('similarity', 0) if mem.metadata else 0
                context += f"{i}. {mem.content} [{sim:.2f}]\n"
            enhanced_task = f"{context}\nUser: {user_input}"
        
        result = await agent.run(task=enhanced_task)
        response = result.messages[-1].content
        print(f"\nAgent: {response}")
        
        # Store conversation
        await memory.session.add(MemoryContent(content=f"User: {user_input}", mime_type=MemoryMimeType.TEXT))
        await memory.session.add(MemoryContent(content=f"Assistant: {response}", mime_type=MemoryMimeType.TEXT))
        
        await memory.vector.add(MemoryContent(
            content=f"Q: {user_input}\nA: {response}",
            mime_type=MemoryMimeType.TEXT))
        
        # Extract and store facts
        print("Extracting facts...")
        facts = await extract_facts(user_input, response)
        
        for fact in facts["user_facts"]:
            await memory.add(MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT), memory_type="semantic", importance=9)
        
        for fact in facts["context_facts"]:
            await memory.add(MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT), memory_type="episodic", importance=5)
        
        if facts["user_facts"] or facts["context_facts"]:
            print(f"Saved: {len(facts['user_facts'])} user facts, {len(facts['context_facts'])} context facts")

if __name__ == "__main__":
    asyncio.run(main())
