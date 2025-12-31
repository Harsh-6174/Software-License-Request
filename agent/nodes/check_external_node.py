import os, requests
from requests.auth import HTTPBasicAuth
from database.db_connection import save_pending_request
from dotenv import load_dotenv

load_dotenv()

def raise_complete_approval_workflow_incident(user_sys_id, software_name, description):
    instance = os.getenv("SERVICENOW_INSTANCE")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident"

    payload = {
        "short_description": f"External software approval required for {software_name}",
        "description": description,
        "caller_id": user_sys_id,
        "category": "software",
        "subcategory": "external_request"
    }

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username,password), headers={"Content-Type": "application/json"})
    return response.json()

def check_external_node(state):
    print("Requested software is not present in Workelevate repo or SAM.")

    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    user_email = state["requester_email"]
    user_sys_id = state["requester_sys_id"]

    description = (
        f"User has requested installation of external software: {software_name}. "
        f"This software is not present in Workelevate repository or SAM. "
        f"Software installation is requested by : {requester_id} - {user_email}"
    )
    state["incident_description"] = description

    if state["is_software_blacklisted"]:
        print("Requested software is blacklisted.")
        state["is_request_valid"] = False
        state["reason_rejection"] = "Requested software is blacklisted and not present in Workelevate repo or SAM."
        return state
    
    print("Requested software requires approval workflow as it is not present in the organization's repo.")
    incident = raise_complete_approval_workflow_incident(user_sys_id, software_name, description)
    state["incident_sys_id"] = incident.get("result", {}).get("sys_id", "")
    print(f"External software incident raised successfully : {incident.get("result", {}).get("number", "invalid")}")

    save_pending_request(
        employee_id = state["requester_id"],
        software = state["software_requested"],
        thread_id = state["thread_id"],
        status = "pending_L1"
    )
    
    state["incident_raised"] = True
    state["is_request_valid"] = True
    state["requires_manager_approval"] = False
    
    return state