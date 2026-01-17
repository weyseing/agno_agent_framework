from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    name="Technical Researcher",
    model=Gemini(id="gemini-2.5-flash-lite"),
    tools=[DuckDuckGoTools()],
    instructions=["Provide technical summaries of search results."],
    markdown=True,   # readable log
    debug_mode=True  # show tracing log
)

agent.print_response(
    "What are the latest specs for NVIDIA Blackwell GPUs?",
    stream=True,
)