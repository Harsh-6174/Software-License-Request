import asyncio
from langgraph.types import Command
from agent.workflow import build_graph

async def run_workflow(app, thread_id, role, initial_state=None):
    config = {"configurable": {"thread_id": thread_id}}

    stream_input = initial_state if role == "employee" else None

    while True:
        async for event in app.astream(stream_input, config, stream_mode="updates"):
            if "__interrupt__" not in event:
                continue

            interrupt_data = event["__interrupt__"][0].value
            prompt = interrupt_data.get("prompt", "")

            print("\n--- WORKFLOW INTERRUPT ---")
            print(prompt)

            user_input = input("> ").strip()
            stream_input = Command(resume=user_input)
            break
        else:
            print("Workflow completed.")
            return