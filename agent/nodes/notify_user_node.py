def notify_user_node(state):
    if state["is_request_valid"] is False:
        print(f"Your request was denied. Reason: {state["reason_rejection"]}")
        return state
    elif state["manager_decision"] != "approved" and state["requires_manager_approval"]:
        print(f"Your request was denied. Reason: {state["reason_rejection"]}")
    else:
        print("Software has been installed")
    
    return state