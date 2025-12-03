import httpx, os
from dotenv import load_dotenv
from microservices.software_name_match import resolve_software_name

load_dotenv()
instance = os.getenv("SERVICENOW_INSTANCE")
username = os.getenv("SERVICENOW_USERNAME")
password = os.getenv("SERVICENOW_PASSWORD")

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
        state["is_requester_id_valid"] = False
        state["is_request_valid"] = False
        state["requires_manager_approval"] = False
        state["reason_rejection"] = "Invalid employee ID"
        return state

    url = f"{instance}/api/now/table/sys_user"
    async with httpx.AsyncClient() as client:
        user_sys_id = await client.get(
            url,
            params = {
                "email": "admin@example.com",
                "sysparm_fields": "sys_id",
                "sysparm_limit": 1
            },
            auth = (username, password)
        )
    data = user_sys_id.json()
    result = data.get("result", [])

    if not result:
        state["is_request_valid"] = False
        state["reason_rejection"] = "User not found in ServiceNow"
        return state
    
    state["requester_sys_id"] = result[0]["sys_id"]
    state["is_requester_id_valid"] = True
    state["is_request_valid"] = True
    
    return state