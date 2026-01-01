from microservices.close_incident import close_incident
from dotenv import load_dotenv

load_dotenv()

async def notify_user_node(state):
    if state["is_request_valid"] is False:
        print(f"1. Your request was denied. Reason: {state["reason_rejection"]}")
        return state
    elif state["requires_manager_approval"] and state["manager_decision"] != "approved":
        print(f"2. Your request was denied. Reason: {state["reason_rejection"]}")
        return state
    else:
        print("Software has been installed")
        if state["manager_decision"] == "approved":
            return state
        
        incident_sys_id = state["incident_sys_id"]
        software_requested = state["software_requested"]
        requester_id = state["requester_id"]
        requester_email = state["requester_email"]
        
        if incident_sys_id:
            closure_note = (f"{software_requested} installation completed for user - {requester_id} {requester_email}. "
                            f"The incident has been closed now.")
            
            payload = {
                "caller": "admin",
                "short_description": f"{software_requested} installation request for user {requester_id} (Resolved)",
                "close_code": "Solution provided",
                "incident_state": "7",
                "close_notes": closure_note,
                "resolved_by": "system"
            }
            await close_incident(incident_sys_id, payload)
        
        return state