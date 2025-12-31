from langgraph.types import interrupt
from microservices.close_incident import close_incident
from microservices.update_incident import update_incident
from database.db_connection import update_request_status

def software_packaging_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    software_source = state["software_source"]
    incident_description = state["incident_description"]

    L3_response = interrupt(
        value={
            "prompt": "L3 Approval required (Final Installation Approval)",
            "request_details": {
                "employee_id" : requester_id,
                "software_requested" : software_name,
                "request_reason" : state["request_reason"],
                "software_source" : software_source,
                "software_restricted" : state["is_software_restricted"],
                "software_blacklisted" : state["is_software_blacklisted"]
            },
            "options": ["Approve", "Deny"]
        }
    )

    if L3_response.lower().startswith("den"):
        reason = interrupt(
            value = {
                "prompt": "Please provide the reason for rejecting this request."
            }
        )

        update_request_status(
            thread_id=state["thread_id"],
            new_status="rejected",
            rejected_by="L3",
            rejection_reason=reason
        )

        if state["incident_sys_id"]:
            payload = {
                "incident_state": "7",
                "close_notes": f"L3 rejected installation of {software_name}. Reason: {reason}"
            }
            close_incident(state["incident_sys_id"], payload)

        return state

    if L3_response.lower().startswith("appr"):
        state["reason_rejection"] = ""
        state["is_request_valid"] = True
        print("Request approved by L3 team.")

        update_request_status(thread_id=state["thread_id"], new_status="approved")

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            update_note = (
                incident_description
                + "\n\n-- Approved by L3 --\n"
                + "Request approved. Ready for software packaging."
            )

            payload = {
                "description": update_note
            }
            update_incident(state["incident_sys_id"], payload)

        return state

    return state