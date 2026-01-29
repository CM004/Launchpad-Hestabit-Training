import asyncio
import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_core.memory import MemoryContent, MemoryMimeType

from session_memory import SessionMemory
from longterm_memory import LongTermMemory
from fact_extractor import  extract_facts, existing_user_facts

async def main():
    os.makedirs("db", exist_ok=True)

    session = SessionMemory(max_turns=5)
    longterm = LongTermMemory(db_path="db/long_term.db")
    
    existing_facts = longterm.get_all_semantic_facts()
    for fact in existing_facts:
        fact_normalized = fact.lower().replace(' ', '')
        existing_user_facts.add(fact_normalized)

    agent = AssistantAgent(
        name="Agent",
        model_client=OllamaChatCompletionClient(model="qwen2.5:7b-instruct-q4_0"),
        memory=[session, longterm],
        system_message="You are a helpful assistant with memory."
    )
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input == 'quit':
            print("Goodbye!")
            break
        
        if user_input == 'debug':
            # Show session memory
            session_result = await session.query("")
            print(f"Messages in session memory: ({len(session_result.results)})")
            for i, mem in enumerate(session_result.results, 1):
                print(f"{i}. {mem.content[:60]}")
            
            # Show user facts
            user_facts = await longterm.query(memory_type="semantic", limit=5)
            print(f"User Facts:({len(user_facts.results)})")
            for i, fact in enumerate(user_facts.results, 1):
                print(f"{i}. {fact.content}")
            
            context_facts = await longterm.query(memory_type="episodic", limit=10)
            print(f"Context: ({len(context_facts.results)})")
            for i, fact in enumerate(context_facts.results, 1):
                print(f"{i}. {fact.content}")
            continue
        
        if user_input == 'stats':
            session_result = await session.query("")
            print(f"Memory Statistics:")
            print(f"Session: {len(session_result.results)} messages")
            print(f"User Facts: {longterm.count('semantic')}")
            print(f"Context: {longterm.count('episodic')}")
            print(f"Total: {longterm.count()}")
            continue
        
        if user_input == 'clear':
            await session.clear()
            await longterm.clear()
            existing_user_facts.clear()
            print("All memories cleared!")
            continue
        
        if not user_input:
            continue
        
        # Get response from agent
        result = await agent.run(task=user_input)
        response = result.messages[-1].content
        print(f"\nAgent: {response}\n")
        
        # Store in session memory (raw conversation)
        await session.add(MemoryContent(content=f"User: {user_input}", mime_type=MemoryMimeType.TEXT))
        await session.add(MemoryContent(content=f"Assistant: {response}", mime_type=MemoryMimeType.TEXT))
        
        # Extract and classify facts
        print("Extracting facts...")
        facts = await extract_facts(user_input, response)
        
        # Store user facts in long-term (semantic memory)
        for fact in facts["user_facts"]:
            await longterm.add(
                MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT),
                memory_type="semantic",
                importance=9
            )
        
        # Store context in long-term (episodic memory)
        for fact in facts["context_facts"]:
            await longterm.add(
                MemoryContent(content=fact, mime_type=MemoryMimeType.TEXT),
                memory_type="episodic",
                importance=5
            )
        
        if facts["user_facts"] or facts["context_facts"]:
            print(f"Saved: {len(facts['user_facts'])} user facts, {len(facts['context_facts'])} context facts")

if __name__ == "__main__":
    os.makedirs("db", exist_ok=True)
    asyncio.run(main())
