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
    else:
        state["is_request_valid"] = True
    
    return state