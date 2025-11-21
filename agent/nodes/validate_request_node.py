import httpx
from microservices.software_name_match import resolve_software_name

async def check_employee_id(requester_id):
    # prompt = f"""
    # You have to check whether an employee is part of our organization or not. 
    # The employee IDs will look like "PR1234", "PR2351", "WE5466", "CE4455".
    # The Employee IDs can be in lowercase so treat them similar.
    # Respond with only one word - "Valid" or "Invalid".

    # Employee ID to check is - {requester_id}
    # """

    # output = llm.invoke(prompt).content.strip().lower()
    # return output == "valid"
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "http://localhost:8000/check-user",
            params = {
                "employee_id" : requester_id
            }
        )
        return res.json()

async def validate_request_node(state):
    requester_id = state["requester_id"]
    # if not is_valid_requester_id(requester_id):
    #     state["is_request_valid"] = False
    #     state["requires_manager_approval"] = False
    #     state["reason_rejection"] = "Invalid employee ID"
    #     return state
    data = await check_employee_id(requester_id)
    result = data["exists"]
    print("---------------------------------------------------------------------------")
    print(f"User Exists? - {result}")
    
    if result is False:
        state["is_request_valid"] = False
        state["requires_manager_approval"] = False
        state["reason_rejection"] = "Invalid employee ID"
        return state

    req = state["software_requested"].lower()
    best_match, category = resolve_software_name(req)

    print(f"Best Software Match : {best_match}")

    if category == "whitelist":
        state["is_request_valid"] = True
        state["requires_manager_approval"] = False
    elif category == "blacklist":
        state["is_request_valid"] = False
        state["requires_manager_approval"] = False
        state["reason_rejection"] = "Software is blacklisted"
    elif category == "requires_manager_approval":
        state["is_request_valid"] = True
        state["requires_manager_approval"] = True
    else:
        print("No category detected, going to manager.........")
        state["is_request_valid"] = True
        state["requires_manager_approval"] = True
    
    return state