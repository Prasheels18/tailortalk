from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
from langchain_groq import ChatGroq
from composio_langchain import ComposioToolSet

# Load env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Request schema
class PromptRequest(BaseModel):
    prompt: str

# LLM and tools (can be reused for multiple requests)
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
composio_toolset = ComposioToolSet(api_key=COMPOSIO_API_KEY)
tools = composio_toolset.get_tools(actions=[
    "GOOGLECALENDAR_CREATE_EVENT",
    "GOOGLECALENDAR_FIND_FREE_SLOTS",
    "GOOGLECALENDAR_EVENTS_LIST"
])
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@app.post("/run")
async def run_agent(request: PromptRequest):
    try:
        response = agent.run(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


