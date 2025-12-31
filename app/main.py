import uuid, asyncio
from agent.workflow import build_graph
from app.auth import login
# from agent.main import run_software_request_workflow
from agent.main import run_workflow
from database.db_connection import get_employee_requests, get_pending_requests

def main():
    app = build_graph()
    user = login()
    role = user["role"]

    # ---------------- EMPLOYEE ----------------
    if role == "employee":
        while True:
            print("\n=== Employee Menu ===")
            print("1. Raise New Software Request")
            print("2. View My Requests")
            print("3. Logout")

            choice = input("> ").strip()

            if choice == "1":
                thread_id = f"req_{user['employee_id']}_{uuid.uuid4().hex}"

                initial_state = {
                    "requester_id": user["employee_id"],
                    "role": role,
                    "thread_id": thread_id,
                    "requester_email": "admin@example.com",
                    "requester_sys_id": "",
                    "incident_sys_id": "",
                    "incident_description": "",
                    "is_requester_id_valid": None,
                    "software_requested": "",
                    "request_reason": "",
                    "is_request_valid": False,
                    "requires_manager_approval": False,
                    "software_source": "",
                    "software_type": "",
                    "security_approval": None,
                    "network_approval": None,
                    "sam_approval": None,
                    "is_software_restricted": False,
                    "is_software_blacklisted": False,
                    "manager_decision": "",
                    "reason_rejection": "",
                    "llm_response": {}
                }

                run_workflow(app, thread_id, "employee", initial_state)

            elif choice == "2":
                pending_requests = get_employee_requests(user['employee_id'])
                if not pending_requests:
                    print("No pending requests.")
                    # return
                    continue

                print("Your Requests:")
                for idx, req in enumerate(pending_requests, 1):
                    print(f"{idx}. {req['software']} | {req['status']}")
            
            elif choice == "3":
                print("Logging out.")
                break

            else:
                print("Invalid option.")


    # ---------------- MANAGER ----------------
    elif role == "manager":
        while True:
            print("\n=== Manager Menu ===")
            print("1. View Pending Approvals")
            print("2. Logout")

            choice = input("> ").strip()

            if choice == "1":
                pending_requests = get_pending_requests("manager")

                if not pending_requests:
                    print("No pending requests.")
                    continue

                print("\nPending Requests:")
                for idx, req in enumerate(pending_requests, 1):
                    print(f"{idx}. {req['employee_id']} requested {req['software']} (thread: {req['thread_id']})")

                selection = int(input("\nSelect a request: ").strip()) - 1
                chosen = pending_requests[selection]

                thread_id = chosen["thread_id"]

                print("\nResuming workflow...")

                config = {"configurable": {"thread_id": thread_id}}
                app.update_state(config=config, values={"role": "manager"})

                run_workflow(app, thread_id, "manager")

            elif choice == "2":
                print("Logging out.")
                break

            else:
                print("Invalid option.")

    # ---------------- OTHER APPROVER TYPES (security, network, etc.) ----------------
    else:
        while True:
            print(f"\n=== {role} Approval Menu ===")
            print("1. View Pending Approvals")
            print("2. Logout")

            choice = input("> ").strip()

            if choice == "1":
                pending_requests = get_pending_requests(role)

                if not pending_requests:
                    print("No pending requests.")
                    continue

                print("\nPending Requests:")
                for idx, req in enumerate(pending_requests, 1):
                    print(f"{idx}. {req['employee_id']} requested {req['software']} (thread: {req['thread_id']})")

                selection = int(input("\nSelect a request: ").strip()) - 1
                chosen = pending_requests[selection]

                thread_id = chosen["thread_id"]

                print("\nResuming workflow...")

                config = {"configurable": {"thread_id": thread_id}}
                app.update_state(config=config, values={"role": role})

                run_workflow(app, thread_id, role)

            elif choice == "2":
                print("Logging out.")
                break

            else:
                print("Invalid option.")

main()