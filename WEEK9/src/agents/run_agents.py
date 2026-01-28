import asyncio
from research_agent import research_agent
from summarizer_agent import summarizer_agent
from answer_agent import answer_agent

async def main():
    query = "write full code in python to implement bfs"

    print("\nResearch Agent working...\n")
    research_response = await research_agent.run(task=query)
    research_result = research_response.messages[-1].content
    print(research_result)

    print("\nSummarizer Agent working...\n")
    summary_response = await summarizer_agent.run(task=research_result)
    summary_result = summary_response.messages[-1].content
    print(summary_result)

    print("\nAnswer Agent working...\n")
    answer_response = await answer_agent.run(task=summary_result)
    answer_result = answer_response.messages[-1].content
    print(answer_result)

if __name__ == "__main__":
    asyncio.run(main())