from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "app/memory/chroma_store"

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vectorstore = Chroma(
    collection_name="startup_memory",
    embedding_function=embeddings,
    persist_directory=CHROMA_PATH
)


def save_memory(content: str, metadata: dict = {}) -> None:
    """
    Saves a piece of information to the vector store.
    metadata can include keys like: startup_name, type (e.g. 'checkpoint', 'research')
    """
    doc = Document(page_content=content, metadata=metadata)
    vectorstore.add_documents([doc])


def retrieve_memory(query: str, k: int = 3) -> str:
    """
    Retrieves the k most relevant memories for a given query.
    Returns them as a single formatted string.
    """
    results = vectorstore.similarity_search(query, k=k)

    if not results:
        return "No relevant memory found."

    formatted = []
    for r in results:
        meta = r.metadata
        formatted.append(f"[{meta}]\n{r.page_content}")

    return "\n\n".join(formatted)


# Quick test
if __name__ == "__main__":

    # Save some startup context
    save_memory(
        "RECRU is an AI-powered recruitment startup based in Portugal. "
        "They are building a platform to match candidates using LLMs. "
        "Main challenge: enterprise sales cycle is too long.",
        metadata={"startup": "RECRU", "type": "checkpoint"}
    )

    save_memory(
        "HeyJobs and Harver are the main competitors of RECRU in Europe.",
        metadata={"startup": "RECRU", "type": "research"}
    )

    # Retrieve it
    result = retrieve_memory("What do we know about RECRU?")
    print(result)