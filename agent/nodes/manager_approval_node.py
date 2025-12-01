from langgraph.types import interrupt
from dotenv import load_dotenv
import os, requests
from requests.auth import HTTPBasicAuth

load_dotenv()

def raise_manager_approval_incident(user_sys_id, software_name, description):
    print("---------------------------------------------------------------------------")
    print("Approval request (case-2: Manager approval required).")
    instance = os.getenv("SERVICENOW_INSTANCE")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident"

    payload = {
        "short_description": f"Manager approval required for {software_name}",
        "description": description,
        "caller_id": user_sys_id,
        "category": "software",
        "subcategory": "installation"
    }

    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username,password), headers={"Content-Type": "application/json"})
    return response.json()

def manager_approval_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    user_email = state["requester_email"]
    user_sys_id = state["requester_sys_id"]
    software_source = state["software_source"]
    software_type = state["software_type"]
    incident_raised = state["incident_raised"]
    state["is_request_valid"] = True

    description = (f"User has requested installation of {software_name}. "
                   f"The software is classified as {software_type} and requires manager approval. "
                   f"The software is detected in {software_source} repository. "
                   f"Software installation is requested by : {requester_id} - {user_email}")
    
    state["incident_description"] = description

    manager_approval_condition = ((software_source == "workelevate" and software_type == "licensed") or 
    (software_source == "sam" and state["is_software_restricted"] is True and state["is_software_blacklisted"] is False))

    if manager_approval_condition and incident_raised is False:
        print("Just before raising ticket")
        incident = raise_manager_approval_incident(user_sys_id, software_name, description)
        state["incident_raised"] = True
        print(f"Incident for manager approval raised successfully : ")
    
    manager_response = interrupt(
        value = {
            "prompt" : "Manager Approval is required",
            "request_details" : {
                "employee_id" : requester_id,
                "software_requested" : software_name,
                "request_reason" : state["request_reason"],
                "software_source" : software_source,
                "software_restricted" : state["is_software_restricted"],
                "software_blacklisted" : state["is_software_blacklisted"],
            },
            "options" : ["Approve", "deny"]
        }
    )

    if manager_response.lower().startswith("den"):
        reason = interrupt(
            value = {
                "prompt": "Please provide the reason for rejecting this request."
            }
        )
        state["manager_decision"] = "denied"
        state["reason_rejection"] = reason or "Not Provided."
        return state

    if manager_response.lower().startswith("appr"):
        state["manager_decision"] = "approved"
        state["is_request_valid"] = True
        state["reason_rejection"] = ""
        print("Request approved by manager.")
        return state

    state["manager_decision"] = "denied"
    state["reason_rejection"] = "Unknown Manager Response"
    print("Unknown manager response - defaulting to request denied.")
    return state