import argparse
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from dotenv import load_dotenv

load_dotenv()

def run_agent_team(query: str):
    researcher = Agent(
        name="Research Agent",
        model=Gemini(id="gemini-2.5-flash"),
        instructions=[
            "Search for facts and break down the core components of the query.",
            "Provide detailed technical points."
        ],
    )

    summarizer = Agent(
        name="Summary Agent",
        model=Gemini(id="gemini-2.5-flash"),
        instructions=[
            "Take the research findings and create a high-level summary.",
            "Keep the final answer concise and user-friendly."
        ],
    )

    agent_team = Team(
        name="Knowledge Team",
        members=[researcher, summarizer],
        model=Gemini(id="gemini-2.5-flash"),
        instructions=[
            "First, let the Research Agent analyze the topic.",
            "Then, let the Summary Agent synthesize that research into the final answer."
        ],
        markdown=True,
    )

    agent_team.print_response(query, stream=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="Question for the agent team")
    args = parser.parse_args()

    run_agent_team(args.query)