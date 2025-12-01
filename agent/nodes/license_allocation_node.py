import requests, os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

def raise_license_allocation_incident(user_sys_id, software_name, description):
    print("---------------------------------------------------------------------------")
    print("Software license allocation (case-1: auto-approved).")
    instance = os.getenv("SERVICENOW_INSTANCE")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident"

    payload = {
        "short_description": f"Software installation request for {software_name}",
        "description": description,
        "caller_id": user_sys_id,
        "category": "software",
        "subcategory": "installation",
    }

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username,password), headers={"Content-Type": "application/json"})
    return response.json()

def license_allocation_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    user_email = state["requester_email"]
    user_sys_id = state["requester_sys_id"]
    software_source = state["software_source"]
    software_type = state["software_type"]
    state["is_request_valid"] = True

    description = (f"User has requested installation of {software_name}. " 
    f"The software is classified as {software_type} and is already approved. " 
    f"The software is detected in {software_source} repository. " 
    f"Software installation is requested by : {requester_id} - {user_email}")

    state["incident_description"] = description

    auto_approved_condition = ((state["software_source"] == "workelevate" and state["software_type"] == "standard") or 
    (state["software_source"] == "sam" and state["is_software_restricted"] is False and state["is_software_blacklisted"] is False))

    if auto_approved_condition:
        if state["manager_decision"] == "approved":
            print("Wrongly reached License allocation")
        incident = raise_license_allocation_incident(user_sys_id, software_name, description)
        print(f"Incident for license allocation raised successfully : {incident.get("result", {}).get("number", "invalid")}")

    return state