import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from agno.db.base import SessionType

db = SqliteDb(
    db_file="/app/tmp/agno.db",
    session_table="agent_sessions"
)

agent = Agent(
    model=Gemini(id="gemini-2.5-flash-lite"),
    db=db
)

def manage_sessions():
    print("--- Current Saved Sessions ---")
    sessions = db.get_sessions(session_type=SessionType.AGENT)
    if not sessions:
        print("No sessions found.")
        return

    # print sessions
    for session in sessions:
        s_id = session.session_id
        print(f"\n{'='*50}")
        print(f"ID: {s_id} | Created: {session.created_at}")
        print(f"{'='*50}")

        # session chats
        chat_history = agent.get_chat_history(session_id=s_id)
        if not chat_history:
            print("[Empty Session]")
            continue
        for msg in chat_history:
            role = msg.role.upper()
            content = msg.content
            print(f"[{role}]: {content}")
            print("-" * 20)

if __name__ == "__main__":
    manage_sessions()