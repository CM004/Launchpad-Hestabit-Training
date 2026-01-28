import asyncio
from orchestrator_day3 import run_orchestration, summarize_results

async def main():
    user_query = "Analyze sales.csv and generate 5 insights from it and write it to output.txt"
    #user_query = "Convert sales.csv to sales.db and save it"
    #user_query="display sales.db table"
    print(f"USER QUERY: {user_query}")

    context = await run_orchestration(user_query)
    
    print("FINAL SUMMARY")
    summary = await summarize_results(context)
    print(summary)

if __name__ == "__main__":
    asyncio.run(main())
