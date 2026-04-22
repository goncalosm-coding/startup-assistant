from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

response = llm.invoke([HumanMessage(content="You are an assistant for startup founders. Say hello and introduce yourself in 2 sentences.")])

print(response.content)