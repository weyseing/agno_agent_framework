import os
import sys
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb

# fast api
app = FastAPI(title="Agno Agent OS API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# storage DB
db = SqliteDb(
    db_file="tmp/agno.db",
    session_table="agent_sessions"
)

# chat request
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_user"

# agent
def get_agent():
    return Agent(
        model=Gemini(id="gemini-2.5-flash-lite"),
        db=db,
        add_history_to_context=True,
        num_history_runs=3,
        markdown=True
    )

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    agent = get_agent()

    def stream_generator():
        response_generator = agent.run(
            request.message, 
            session_id=request.session_id, 
            stream=True
        )
        
        for chunk in response_generator:
            if chunk.content:
                yield chunk.content

    return StreamingResponse(stream_generator(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent_os.fastapi_stream:app", host="0.0.0.0", port=8000, reload=True)