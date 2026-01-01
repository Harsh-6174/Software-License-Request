from langgraph.types import interrupt
from microservices.close_incident import close_incident
from microservices.update_incident import update_incident
from database.db_connection import update_request_status

async def security_network_approval_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    software_source = state["software_source"]
    incident_description = state["incident_description"]

    L1_response = interrupt(
        value={
            "prompt": "L1 Approval required (Security + Network)",
            "request_details": {
                "employee_id": requester_id,
                "software_requested": software_name,
                "request_reason": state["request_reason"],
                "software_source": software_source,
                "software_restricted": state["is_software_restricted"],
                "software_blacklisted": state["is_software_blacklisted"],
            },
            "options": ["Approve", "Deny"]
        }
    )

    if L1_response.lower().startswith("den"):
        reason = interrupt(
            value={
                "prompt": "Please provide the reason for rejecting this request."
            }
        )

        state["security_approval"] = False
        state["network_approval"] = False
        state["reason_rejection"] = reason or "Not Provided."

        await update_request_status(state["thread_id"], "rejected_L1")

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            closure_note = (
                f"L1 denied request for {software_name} installation. "
                f"Reason : {state['reason_rejection']}."
            )

            payload = {
                "caller": "admin",
                "short_description": f"L1 approval for {software_name} requested by {requester_id} (Rejected)",
                "close_code": "Solution provided",
                "incident_state": "7",
                "close_notes": closure_note,
                "resolved_by": "system"
            }

            await close_incident(incident_sys_id, payload)

        return state

    if L1_response.lower().startswith("appr"):
        state["security_approval"] = True
        state["network_approval"] = True
        state["reason_rejection"] = ""
        state["is_request_valid"] = True

        if state["software_type"] == "licensed":
            await update_request_status(state["thread_id"], "pending_L2")
        else:
            await update_request_status(state["thread_id"], "pending_L3")

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            if state["software_type"] == "standard":
                next_step_note = (
                    "Software classified as STANDARD. "
                    "L2 approval is not required. "
                    "Routing directly to L3 approval."
                )
            else:
                next_step_note = (
                    "Software classified as LICENSED. "
                    "L2 approval is required before proceeding to L3."
                )

            update_note = (
                incident_description
                + "\n\n-- Approved by L1 --\n"
                + next_step_note
            )

            payload = {
                "description": update_note
            }

            await update_incident(incident_sys_id, payload)

        return state

    state["security_approval"] = False
    state["network_approval"] = False
    state["reason_rejection"] = "Unknown L1 Response"
    return state