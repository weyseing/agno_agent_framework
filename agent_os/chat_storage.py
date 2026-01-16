import os
import argparse
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb

# sqlite DB
db = SqliteDb(
    session_table="agent_sessions",
    db_file="/app/tmp/agno.db"
)

# agent
agent = Agent(
    model=Gemini(id="gemini-2.5-flash-lite"),
    description="I am a persistent agent who remembers our past chats.",
    markdown=True,
    debug_mode=True,
    # chat storage
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
)

# sesison ID
session_id = "user_12345"
print(f"--- Session ID: {session_id} ---")

# chat
parser = argparse.ArgumentParser()
parser.add_argument("query", type=str, nargs='?', default="Hi! My favorite color is neon green. Remember that!")
args = parser.parse_args()
agent.print_response(args.query, session_id=session_id)
