from agno.agent import Agent
from agno.models.google import Gemini
from agno.team import Team
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash-lite"

candidate_a = Agent(
    name="Candidate A",
    role="Logical and Mathematical Thinker",
    model=Gemini(id=MODEL_NAME),
    instructions=["Solve the problem step-by-step using first principles."],
)

candidate_b = Agent(
    name="Candidate B",
    role="Creative and Lateral Thinker",
    model=Gemini(id=MODEL_NAME),
    instructions=["Look for hidden patterns or alternative interpretations of the problem."],
)

candidate_c = Agent(
    name="Candidate C",
    role="Critical and Skeptical Thinker",
    model=Gemini(id=MODEL_NAME),
    instructions=["Double-check every assumption and verify the logic for errors."],
)

judge_team = Team(
    name="The High Court",
    members=[candidate_a, candidate_b, candidate_c],
    model=Gemini(id=MODEL_NAME),
    delegate_to_all_members=True,
    instructions=[
        "You will receive three different solutions to the same problem.",
        "1. Compare the solutions for consistency.",
        "2. If they disagree, analyze the logic of each and identify the most mathematically sound one.",
        "3. If all are wrong, provide the correct answer yourself.",
        "4. Output the final 'Verdict' clearly.",
    ],
    show_members_responses=True,
    markdown=True,
)

query = "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?"
judge_team.print_response(query, stream=True)