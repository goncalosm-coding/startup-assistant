from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from app.tools.search import search_web
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

tools = [search_web]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Research Agent specialising in startup ecosystems, 
    market analysis, and competitor intelligence.
    
    When given a research question, you search for relevant information and 
    return a clean, structured summary. Always cite your sources.
    
    Be concise but thorough. Format your response clearly."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # this lets you see the agent's thinking in the terminal
)


def run_research_agent(question: str, chat_history: list = []) -> str:
    result = agent_executor.invoke({
        "input": question,
        "chat_history": chat_history
    })
    return result["output"]


# Quick test
if __name__ == "__main__":
    response = run_research_agent(
        "Who are the top 3 competitors of a startup doing AI-powered recruitment in Europe?"
    )
    print("\n--- FINAL RESPONSE ---")
    print(response)