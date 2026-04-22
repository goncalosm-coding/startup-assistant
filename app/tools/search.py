from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str) -> str:
    """
    Searches the web for the given query and returns a summarised result.
    Used by the Research Agent to find competitor info and market data.
    """
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results = []
    for r in response["results"]:
        results.append(f"Source: {r['url']}\nSummary: {r['content']}\n")

    return "\n".join(results)


# Quick test
if __name__ == "__main__":
    output = search_web("top Incubators and Accelerators in Europe 2026")
    print(output)