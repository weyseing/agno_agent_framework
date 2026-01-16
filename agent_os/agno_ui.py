from agno.agent import Agent
from agno.models.google import Gemini
from agno.os import AgentOS

gemini_agent = Agent(
    name="Gemini OS Agent",
    model=Gemini(
        id="gemini-2.5-flash", 
        thinking_budget=1024,
    ),
    description="I am an agent running on Agno OS powered by Gemini 2.5 Flash.",
    instructions=["Always provide a concise summary of your internal thoughts before answering."],
    markdown=True,
    debug_mode=True
)

agent_os = AgentOS(
    agents=[gemini_agent],
)
app = agent_os.get_app()

if __name__ == "__main__":
    # http://localhost:8000
    agent_os.serve(app="agno_ui:app", host="0.0.0.0", port=7777,reload=True)