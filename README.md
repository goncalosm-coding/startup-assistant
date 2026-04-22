# Startup Assistant — Multi-Agent AI System

A multi-agent AI system built for startup founders. It researches competitors, drafts documents, and remembers context across sessions — all through a single API or chat interface.

## Architecture

```
User Input
    ↓
Orchestrator (LangGraph)
    ↓ classifies intent
    ├── Research Agent → Tavily web search → structured answer
    ├── Document Agent → drafts emails, reports, summaries
    └── Memory Agent → ChromaDB vector store → persistent context
```

## Stack

- **LangChain** — agent framework and tool calling
- **LangGraph** — multi-agent orchestration and state management
- **FastAPI** — REST API layer
- **ChromaDB** — vector store for persistent memory
- **Tavily** — real-time web search for the Research Agent
- **Docker** — containerised deployment

## Agents

**Orchestrator** — classifies the user's intent and routes to the right agent using a LangGraph state machine.

**Research Agent** — searches the web in real time and returns structured competitive intelligence and market analysis.

**Document Agent** — produces professional documents: emails, competitor reports, meeting summaries, and investor updates.

**Memory Agent** — stores and retrieves startup context across sessions using semantic similarity search.

## Getting Started

### Prerequisites
- Python 3.9+
- Docker Desktop
- OpenAI API key
- Tavily API key

### Local Development

```bash
git clone https://github.com/goncalosm-coding/startup-assistant.git
cd startup-assistant

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:
```
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key
```

Run the server:
```bash
python -m app.main
```

### Docker

```bash
docker compose up --build
```

### API

Once running, the API is available at `http://localhost:8000`.

Interactive docs: `http://localhost:8000/docs`

**Chat endpoint:**
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Who are the top competitors of a fintech startup in Portugal?"}'
```

## Project Structure

```
startup-assistant/
├── app/
│   ├── agents/
│   │   ├── orchestrator.py     ← LangGraph routing logic
│   │   ├── research_agent.py   ← web search + synthesis
│   │   └── document_agent.py   ← document generation
│   ├── tools/
│   │   └── search.py           ← Tavily search tool
│   ├── memory/
│   │   └── memory_agent.py     ← ChromaDB vector store
│   ├── api/
│   │   ├── main.py             ← FastAPI app
│   │   └── routes.py           ← API endpoints
│   └── main.py                 ← entry point
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```