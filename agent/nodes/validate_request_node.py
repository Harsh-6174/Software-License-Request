import httpx
from microservices.software_name_match import resolve_software_name

async def validate_request_node(state):
    requester_id = state["requester_id"]
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "http://localhost:8000/check-user",
            params = {
                "employee_id" : requester_id
            }
        )
    data = res.json()
    print("---------------------------------------------------------------------------")
    print(f"User Exists? - {data['exists']}")
    
    if data["exists"] is False:
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