from langgraph.types import interrupt
from microservices.close_incident import close_incident

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

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            closure_note = (f"Manager denied request for {software_name} installation. "
                            f"Reason: {state['reason_rejection']}.")
            
            payload = {
                "caller": "admin",
                "short_description": f"Manager approval for {software_name} requested by {requester_id} (Rejected)",
                "close_code": "Solution provided",
                "incident_state": "7",
                "close_notes": closure_note,
                "resolved_by": "system"
            }
            close_incident(incident_sys_id, payload)

        return state

    if manager_response.lower().startswith("appr"):
        state["manager_decision"] = "approved"
        state["is_request_valid"] = True
        state["reason_rejection"] = ""
        print("Request approved by manager.")

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            closure_note = (f"Manager approved request for {software_name} installation.")

            payload = {
                "caller": "admin",
                "short_description": f"Manager approval for {software_name} requested by {requester_id} (Approved)",
                "close_code": "Solution provided",
                "incident_state": "7",
                "close_notes": closure_note,
                "resolved_by": "system"
            }
            close_incident(incident_sys_id, payload)
        
        return state

    state["manager_decision"] = "denied"
    state["reason_rejection"] = "Unknown Manager Response"
    print("Unknown manager response - defaulting to request denied.")
    return state