from tavily import TavilyClient
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_web(query: str) -> str:
    """
    Searches the web for the given query and returns relevant results.
    Use this to find competitor information, market data, industry trends,
    or any information about startups and business topics.
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