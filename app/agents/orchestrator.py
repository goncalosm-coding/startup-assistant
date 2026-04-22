from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict
from dotenv import load_dotenv

from app.agents.research_agent import run_research_agent
from app.agents.document_agent import run_document_agent
from app.memory.memory_agent import retrieve_memory, save_memory

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# --- State definition ---
# This is the object that gets passed between nodes in the graph

class AgentState(TypedDict):
    user_input: str
    intent: str
    memory_context: str
    agent_response: str


# --- Node 1: Retrieve memory ---

def retrieve_memory_node(state: AgentState) -> AgentState:
    context = retrieve_memory(state["user_input"])
    state["memory_context"] = context
    return state


# --- Node 2: Classify intent ---

def classify_intent_node(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an intent classifier. Given a user message, 
        classify it into exactly one of these categories:
        
        - research: user wants to find information, competitors, market data
        - document: user wants to produce a document, email, report, or summary
        - memory: user wants to save information about a startup
        
        Reply with only the category word. Nothing else."""),
        ("human", "{input}")
    ])

    chain = prompt | llm
    result = chain.invoke({"input": state["user_input"]})
    state["intent"] = result.content.strip().lower()
    return state


# --- Node 3: Route to the right agent ---

def research_node(state: AgentState) -> AgentState:
    full_input = f"""
    User request: {state['user_input']}
    
    Relevant context from memory:
    {state['memory_context']}
    """
    state["agent_response"] = run_research_agent(full_input)
    return state


def document_node(state: AgentState) -> AgentState:
    full_input = f"""
    User request: {state['user_input']}
    
    Relevant context from memory:
    {state['memory_context']}
    """
    state["agent_response"] = run_document_agent(full_input)
    return state


def memory_node(state: AgentState) -> AgentState:
    save_memory(state["user_input"])
    state["agent_response"] = "Got it, I've saved that information."
    return state


# --- Routing function ---

def route_intent(state: AgentState) -> str:
    intent = state.get("intent", "research")
    if intent == "document":
        return "document"
    elif intent == "memory":
        return "memory"
    else:
        return "research"


# --- Build the graph ---

graph = StateGraph(AgentState)

graph.add_node("retrieve_memory", retrieve_memory_node)
graph.add_node("classify_intent", classify_intent_node)
graph.add_node("research", research_node)
graph.add_node("document", document_node)
graph.add_node("memory", memory_node)

graph.set_entry_point("retrieve_memory")

graph.add_edge("retrieve_memory", "classify_intent")

graph.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "research": "research",
        "document": "document",
        "memory": "memory"
    }
)

graph.add_edge("research", END)
graph.add_edge("document", END)
graph.add_edge("memory", END)

app = graph.compile()


# --- Public interface ---

def run_orchestrator(user_input: str) -> str:
    result = app.invoke({"user_input": user_input})
    return result["agent_response"]


# Quick test
if __name__ == "__main__":
    questions = [
        "Who are the main competitors of an AI recruitment startup in Europe?",
        "Write a short email to a founder named João summarising that their main challenge is enterprise sales cycles.",
        "Remember that ProcessPlot is a startup doing process automation for factories in Portugal."
    ]

    for q in questions:
        print(f"\n{'='*60}")
        print(f"INPUT: {q}")
        print(f"{'='*60}")
        response = run_orchestrator(q)
        print(f"\nRESPONSE:\n{response}")