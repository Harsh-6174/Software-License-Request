from langgraph.types import interrupt
from database.db_connection import update_request_status
from microservices.update_incident import update_incident
from microservices.close_incident import close_incident

async def sam_approval_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    software_source = state["software_source"]
    incident_description = state["incident_description"]

    L2_response = interrupt(
        value={
            "prompt": "L2 Approval required (SAM)",
            "request_details": {
                "employee_id": requester_id,
                "software_requested": software_name,
                "request_reason": state["request_reason"],
                "software_source": software_source,
                "software_restricted": state["is_software_restricted"],
                "software_blacklisted": state["is_software_blacklisted"]
            },
            "options": ["Approve", "Deny"]
        }
    )

    if L2_response.lower().startswith("den"):
        reason = interrupt(
            value={
                "prompt": "Please provide the reason for rejecting this request."
            }
        )

        state["sam_approval"] = False
        state["reason_rejection"] = reason or "Not Provided."

        await update_request_status(state["thread_id"], "rejected_L2")

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            closure_note = (
                f"L2 denied request for {software_name} installation. "
                f"Reason : {state['reason_rejection']}."
            )

            payload = {
                "caller": "admin",
                "short_description": f"L2 approval for {software_name} requested by {requester_id} (Rejected)",
                "close_code": "Solution provided",
                "incident_state": "7",
                "close_notes": closure_note,
                "resolved_by": "system"
            }

            await close_incident(incident_sys_id, payload)

        return state

    if L2_response.lower().startswith("appr"):
        state["sam_approval"] = True
        state["reason_rejection"] = ""
        state["is_request_valid"] = True

        await update_request_status(state["thread_id"], "pending_L3")

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            update_note = (
                incident_description
                + "\n\n-- Approved by L2 --\n"
                + "Routing to L3 approval."
            )

            payload = {
                "description": update_note
            }

            await update_incident(incident_sys_id, payload)

        return state

    state["sam_approval"] = False
    state["reason_rejection"] = "Unknown L2 Response"
    return state
