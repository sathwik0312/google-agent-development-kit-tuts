import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async

load_dotenv()

#Part-1: Initialize Persistent Session Service
#Using SQLite database for persistent storage
db_url="sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

#Part:2 Define Initial State
#This will only be used when creating a new session
initial_state = {
    "user_name":"sathwik",
    "reminders":[],
}

async def main_async():
    APP_NAME="Memory agent"
    USER_ID="aiwithsathwik"

    #Part 3: Session Management - Find or Create
    existing_sessions=session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    #If there's an existing session, use it, otherwise create a new one
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID=existing_sessions.sessions[0].id
        print(f"Continuing existing session:{SESSION_ID}")
    else:
        new_session=session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID=new_session.id
        print(f"Created a new session:{SESSION_ID}")
    
    #Part 4: Agent runner setup
    runner=Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    #Part 5: Interactive conversation loop
    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        #Get user input
        user_input=input("You:")

        #check if user want to exit
        if user_input.lower() in ["exit","quit"]:
            print("Ending conversation.Your data has been saved to the database")
            break

        #Process the user query through the agent
        await call_agent_async(runner,USER_ID,SESSION_ID,user_input)
    
if __name__=="__main__":
    asyncio.run(main_async())

