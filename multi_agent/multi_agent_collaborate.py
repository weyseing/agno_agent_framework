import argparse
from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash-lite"

def run_collaborative_team(query: str):
    business_analyst = Agent(
        name="Business Analyst",
        role="Analyze the business and market implications",
        model=Gemini(id=MODEL_NAME),
        instructions=["Provide 3 high-level business risks and 3 opportunities."],
    )

    tech_architect = Agent(
        name="Tech Architect",
        role="Analyze technical feasibility and architecture",
        model=Gemini(id=MODEL_NAME),
        instructions=["Identify the best technology stack and potential bottlenecks."],
    )

    compliance_officer = Agent(
        name="Compliance Officer",
        role="Analyze security, privacy, and regulatory risks",
        model=Gemini(id=MODEL_NAME),
        instructions=["Focus on data privacy (GDPR/PDPA) and security vulnerabilities."],
    )

    agent_team = Team(
        name="Executive Strategy Team",
        members=[business_analyst, tech_architect, compliance_officer],
        model=Gemini(id=MODEL_NAME),

        # delegate to all
        delegate_to_all_members=True, 
        instructions=[
            "Review the individual reports from each member.",
            "Synthesize the final strategy."
        ],
        markdown=True,
    )

    agent_team.print_response(query, stream=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, nargs='?', default="Evaluation of a new AI-powered logistics hub in Cyberjaya")
    args = parser.parse_args()

    run_collaborative_team(args.query)