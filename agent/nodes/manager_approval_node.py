from langgraph.types import interrupt
from dotenv import load_dotenv
import os, requests
from requests.auth import HTTPBasicAuth

load_dotenv()

def manager_approval_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    software_source = state["software_source"]
    
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