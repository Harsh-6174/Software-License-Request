import asyncio
from langgraph.types import Command
from agent.workflow import build_graph

# python -m agent.main
async def main(app):
    config = {"configurable": {"thread_id": "user-session-001"}}
    initial_state = {
        "requester_id": "",
        "is_requester_id_valid": None,
        "software_requested": "",
        "request_reason": "",
        "is_request_valid": False,
        "requires_manager_approval": False,
        "software_source": "",
        "software_type": "",
        "is_software_restricted": False,
        "is_software_blacklisted": False,
        "manager_decision": "",
        "reason_rejection": "",
        "llm_response": {}
    }

    input_to_continue = None

    print("----------------------------- Initial State ------------------------------")
    for key,value in initial_state.items():
        print(f"{key} : {value}")

    while True:
        if input_to_continue is None:
            print("----------------------------- Workflow Starting -----------------------------")
            stream_input = initial_state
        else:
            print(f"Resuming with : {input_to_continue}")
            stream_input = Command(resume=input_to_continue)
        
        interrupted = False
        async for event in app.astream(stream_input, config, stream_mode="updates"):
            if "__interrupt__" in event:
                interrupted = True
                prompt_data = event["__interrupt__"][0].value

                print(f"Interrupt: {prompt_data.get('prompt')}")
                if "Manager" in prompt_data.get('prompt', ''):
                    print(f"Request Details : {prompt_data.get('request_details', [])}")
                    print(f"Options: {prompt_data.get('options', [])}")
                input_to_continue = input("Your input: ") or "Not Provided."
                break
        
        if not interrupted:
            print("----------------------------- Workflow completed -----------------------------")
            break

app = build_graph()

image = app.get_graph().draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(image)

asyncio.run(main(app))