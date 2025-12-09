import uuid, asyncio
from app.auth import login
from agent.main import run_software_request_workflow

async def main():
    user = login()

    role = user["role"]

    if role == "employee":
        print("\n=== Employee Menu ===")
        print("1. Raise New Software Request")
        print("2. View My Requests")
        print("3. Logout")

        choice = input("> ")

        if choice == "1":
            thread_id = f"req_{user['employee_id']}_{uuid.uuid4().hex}"
            await run_software_request_workflow(user["employee_id"], thread_id)
        elif choice == "2":
            print("View request flow will come here.")
        else:
            print("Goodbye.")
    elif role == "manager":
        print("\n=== Manager Menu ===")
        print("1. View Pending Approvals")
        print("2. Logout")

        choice = input("> ")

        if choice == "1":
            print("Approval list will come later.")
        else:
            print("Goodbye.")
    else:
        role = user["role"]
        print(f"\n=== {role} Approval Menu ===")
        print("1. View Pending Approvals")
        print("2. Logout")

        choice = input("> ")

        if choice == "1":
            print("Approver list will come here.")
        else:
            print("Goodbye.")

asyncio.run(main())