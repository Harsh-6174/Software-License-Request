from langgraph.types import interrupt
from microservices.close_incident import close_incident
from microservices.update_incident import update_incident
from database.db_connection import update_request_status

def raise_external_software_incident():
    print("---------------------------------------------------------------------------")
    print("External software approval request (case-3: Escalation Approval).")

# def security_network_approval_node(state):
#     requester_id = state["requester_id"]
#     software_name = state["software_requested"]
#     user_email = state["requester_email"]
#     user_sys_id = state["requester_sys_id"]

#     state["is_request_valid"] = True



#     security_response = interrupt(
#         value = {
#             "prompt": "L1 - Security Approval is required",
#             "request_details": {
#                 "employee_id": requester_id,
#                 "software_requested": software_name,
#                 "request_reason": state["request_reason"],
#                 "software_restricted" : state["is_software_restricted"],
#                 "software_blacklisted" : state["is_software_blacklisted"]
#             },
#             "options": ["Approve", "Deny"]
#         }
#     )

#     if security_response.lower().startswith("den"):
#         reason = interrupt(
#             value = {
#                 "prompt": "Please provide the reason for rejecting this request."
#             }
#         )

#         state["security_approval"] = False
#         state["reason_rejection"] = reason or "Not Provided"

#         incident_sys_id = state["incident_sys_id"]
#         if incident_sys_id:
#             closure_note = (
#                 f"Security Team denied request for {software_name} installation. "
#                 f"Reason: {state["reason_rejection"]}"
#             )

#             payload = {
#                 "caller": "admin",
#                 "short_description": f"External software request for {software_name} requested by {requester_id} (Rejected)",
#                 "close_code": "",
#                 "incident_state": "7",
#                 "close_notes": closure_note,
#                 "resolved_by": "system"
#             }
#             close_incident(incident_sys_id, payload)
        
#         return state

#     if security_response.lower().startswith("appr"):
#         state["security_approval"] = True
#         print("Request approved by security team.")

#         incident_sys_id = state["incident_sys_id"]
#         if incident_sys_id:
#             if state["software_type"] == "licensed":
#                 updation_note = (
#                     f"Security team approved {software_name} request. "
#                     f"Forwarding request for SAM approval. "
#                 )

#                 payload = {
#                     "caller": "admin",
#                     "short_description": f""
#                 }

#             else:
#                 updation_note = (
#                     f"Security team approved {software_name} request. "
#                     f"Forwarding request for software packaging. "
#                 )

#                 payload = {
#                     "caller": "admin",
#                     "short_description": f""
#                 }
            
#             update_incident(incident_sys_id, payload)
        
#         return state
    

    
#     network_response = interrupt(
#         value = {
#             "prompt": "L1 - Security Approval is required",
#             "request_details": {
#                 "employee_id": requester_id,
#                 "software_requested": software_name,
#                 "request_reason": state["request_reason"],
#                 "software_restricted" : state["is_software_restricted"],
#                 "software_blacklisted" : state["is_software_blacklisted"]
#             },
#             "options": ["Approve", "Deny"]
#         }
#     )

#     if network_response.lower().startswith("den"):
#         reason = interrupt(
#             value = {
#                 "prompt": "Please provide the reason for rejecting this request."
#             }
#         )

#         state["network_approval"] = False
#         state["reason_rejection"] = reason or "Not Provided"

#         incident_sys_id = state["incident_sys_id"]
#         if incident_sys_id:
#             closure_note = (
#                 f""
#             )





#     description = (
#         f"User has requested installation of {software_name}. "
#         f"The software is not present in Workelevate repository and SAM repository, and requires complete approval workflow. "
#         f"Software installation is requested by : {requester_id} - {user_email}"
#     )

#     state["incident_description"] = description

#     print("Creating External Approval Incident")
#     incident = raise_external_software_incident(user_sys_id, software_name, description)
#     state["incident_raised"] = True
#     state["incident_sys_id"] = incident.get("result", {}).get("sys_id", "")
#     print(f"Incident created: {incident.get('result', {}).get('number', 'invalid')}")

















# def security_network_approval_node(state):
#     requester_id = state["requester_id"]
#     software_name = state["software_requested"]
#     user_email = state["requester_email"]
#     user_sys_id = state["requester_sys_id"]

#     if state["security_approval"] is None:

#         security_response = interrupt(
#             value={
#                 "prompt": "L1 - Security Approval is required",
#                 "request_details": {
#                     "employee_id": requester_id,
#                     "software_requested": software_name,
#                     "request_reason": state["request_reason"],
#                     "software_restricted": state["is_software_restricted"],
#                     "software_blacklisted": state["is_software_blacklisted"]
#                 },
#                 "options": ["Approve", "Deny"]
#             }
#         )

#         if security_response.lower().startswith("den"):
#             reason = interrupt(
#                 value={"prompt": "Please provide the reason for rejecting this request."}
#             )

#             state["security_approval"] = False
#             state["reason_rejection"] = reason or "Not Provided"

#             if state.get("incident_sys_id"):
#                 payload = {
#                     "caller": "admin",
#                     "short_description": f"Security rejected {software_name} request by {requester_id}",
#                     "close_code": "Rejected by Security",
#                     "incident_state": "7",
#                     "close_notes": f"Security denied {software_name}. Reason: {state['reason_rejection']}.",
#                     "resolved_by": "system"
#                 }
#                 close_incident(state["incident_sys_id"], payload)

#             return state

#         state["security_approval"] = True

#     if state["network_approval"] is None:

#         network_response = interrupt(
#             value={
#                 "prompt": "L1 - Network Approval is required",
#                 "request_details": {
#                     "employee_id": requester_id,
#                     "software_requested": software_name,
#                     "request_reason": state["request_reason"],
#                     "software_restricted": state["is_software_restricted"],
#                     "software_blacklisted": state["is_software_blacklisted"]
#                 },
#                 "options": ["Approve", "Deny"]
#             }
#         )

#         if network_response.lower().startswith("den"):
#             reason = interrupt(
#                 value={"prompt": "Please provide the reason for rejecting this request."}
#             )

#             state["network_approval"] = False
#             state["reason_rejection"] = reason or "Not Provided"

#             if state.get("incident_sys_id"):
#                 payload = {
#                     "caller": "admin",
#                     "short_description": f"Network rejected {software_name} request by {requester_id}",
#                     "close_code": "Rejected by Network",
#                     "incident_state": "7",
#                     "close_notes": f"Network denied {software_name}. Reason: {state['reason_rejection']}.",
#                     "resolved_by": "system"
#                 }
#                 close_incident(state["incident_sys_id"], payload)

#             return state

#         state["network_approval"] = True

#     print("Final value of Security Approval : ",state["security_approval"])
#     print("Final value of network Approval : ",state["network_approval"])
#     return state





def security_network_approval_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    software_source = state["software_source"]
    incident_description = state["incident_description"]

    L1_response = interrupt(
        value = {
            "prompt" : "L1 Approval required (Security + Network)",
            "request_details" : {
                "employee_id" : requester_id,
                "software_requested" : software_name,
                "request_reason" : state["request_reason"],
                "software_source" : software_source,
                "software_restricted" : state["is_software_restricted"],
                "software_blacklisted" : state["is_software_blacklisted"],
            },
            "options" : ["Approve", "Deny"]
        }
    )

    if L1_response.lower().startswith("den"):
        reason = interrupt(
            value = {
                "prompt" : "Please provide the reason for rejecting this request."
            }
        )

        state["security_approval"] = False
        state["network_approval"] = False
        state["reason_rejection"] = reason or "Not Provided."

        update_request_status(state["thread_id"], "rejected_L1")

        incident_sys_id = state["incident_sys_id"]
        if incident_sys_id:
            closure_note = (f"L1 denied request for {software_name} installation. "
                            f"Reason : {state['reason_rejection']}.")
            
            payload = {
                "caller": "admin",
                "short_description": f"L1 approval for {software_name} requested by {requester_id} (Rejected)",
                "close_code": "Solution provided",
                "incident_state": "7",
                "close_notes": closure_note,
                "resolved_by": "system"
            }
            close_incident(incident_sys_id, payload)

        return state
    
    if L1_response.lower().startswith("appr"):
        state["security_approval"] = True
        state["network_approval"] = True
        state["reason_rejection"] = ""
        state["is_request_valid"] = True
        print("Request approved by L1 team.")

        # update_request_status(state["thread_id"], "approved_L1")
        if state["software_type"] == "licensed":
            update_request_status(state["thread_id"], "pending_L2")
        else:
            update_request_status(state["thread_id"], "pending_L3")

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
            update_incident(incident_sys_id, payload)

        return state
    
    state["security_approval"] = False
    state["network_approval"] = False
    state["reason_rejection"] = "Unknown L1 Response"
    print("Unknown L1 response - defaulting to request denied.")
    return state