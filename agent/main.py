import asyncio
from langgraph.types import Command
from agent.workflow import build_graph

# app = build_graph()

# async def run_software_request_workflow(app, requester_id: str, thread_id: str):
#     config = {"configurable": {"thread_id": thread_id}}
#     initial_state = {
#         "requester_id": requester_id,
#         "thread_id": thread_id,
#         "requester_email": "admin@example.com",
#         "requester_sys_id": "",
#         "incident_sys_id": "",
#         "incident_raised": False,
#         "is_requester_id_valid": None,
#         "software_requested": "",
#         "request_reason": "",
#         "is_request_valid": False,
#         "requires_manager_approval": False,
#         "software_source": "",
#         "software_type": "",
#         "security_approval": None,
#         "network_approval": None,
#         "sam_approval": None,
#         "is_software_restricted": False,
#         "is_software_blacklisted": False,
#         "manager_decision": "",
#         "reason_rejection": "",
#         "llm_response": {}
#     }

#     input_to_continue = None

#     print("----------------------------- Initial State ------------------------------")
#     for key,value in initial_state.items():
#         print(f"{key} : {value}")

#     while True:
#         if input_to_continue is None:
#             print("----------------------------- Workflow Starting -----------------------------")
#             stream_input = initial_state
#         else:
#             print(f"Resuming with : {input_to_continue}")
#             stream_input = Command(resume=input_to_continue)
        
#         interrupted = False
#         async for event in app.astream(stream_input, config, stream_mode="updates"):
#             if "__interrupt__" in event:
#                 interrupted = True
#                 prompt_data = event["__interrupt__"][0].value

#                 print(f"Interrupt: {prompt_data.get('prompt')}")

#                 if prompt_data.get('prompt') == "Manager approval required. Request is now pending for approval":
#                     current_state = await app.aget_state(config={"configurable": {"thread_id": thread_id}})
#                     current_state = current_state.values
#                     employee_id = current_state["requester_id"]
#                     software = current_state["software_requested"]

#                     save_pending_manager_request(
#                         employee_id=employee_id,
#                         software=software,
#                         thread_id=thread_id
#                     )

#                     print("Request saved in DB. Waiting for manager approval.")
#                     return

#                 if "Manager" in prompt_data.get('prompt', ''):
#                     print(f"Request Details : {prompt_data.get('request_details', [])}")
#                     print(f"Options: {prompt_data.get('options', [])}")
#                 input_to_continue = input("Your input: ") or "Not Provided."
#                 break
        
#         if not interrupted:
#             print("----------------------------- Workflow completed -----------------------------")
#             break

# image = app.get_graph().draw_mermaid_png()
# with open("graph.png", "wb") as f:
#     f.write(image)

















# def run_workflow(app, thread_id, role, initial_state=None):
#     config = {"configurable": {"thread_id": thread_id}}

#     # stream_input = initial_state if role == "employee" else Command(resume=True)
#     stream_input = initial_state if role == "employee" else None

#     while True:
#         print("Just entered while loop")
#         for event in app.stream(stream_input, config, stream_mode="updates"):
#             print("Just entered for loop")

#             print("Before __interrupt__")
#             if "__interrupt__" not in event:
#                 continue
#             print("After __interrupt__")
            
#             interrupt_data = event["__interrupt__"][0].value
#             prompt = interrupt_data.get("prompt", "")

#             print("\n--- WORKFLOW INTERRUPT ---")
#             print(prompt)

#             if role == "employee" and "Manager Approval" in prompt:
#                 state = app.get_state(config=config).values

#                 save_pending_manager_request(
#                     employee_id=state["requester_id"],
#                     software=state["software_requested"],
#                     thread_id=thread_id
#                 )

#                 print("Request saved. Waiting for manager approval.")
#                 return
            
#             elif role == "employee" and "L1 approval" in prompt:
#                 state = app.get_state(config=config).values

#                 save_pending_manager_request(
#                     employee_id=state["requester_id"],
#                     software=state["software_requested"],
#                     status = "pending_L1",
#                     thread_id=thread_id
#                 )

#                 print("Request saved. Waiting for L1 approval.")
#                 return
            
#             # elif role == "manager" and "Manager Approval" in prompt:
                

#             user_input = input("Your response: ").strip()
#             stream_input = Command(resume=user_input)
#             break

#         else:
#             print("Workflow completed.")
#             return























def run_workflow(app, thread_id, role, initial_state=None):
    config = {"configurable": {"thread_id": thread_id}}

    stream_input = initial_state if role == "employee" else None

    while True:
        for event in app.stream(stream_input, config, stream_mode="updates"):
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