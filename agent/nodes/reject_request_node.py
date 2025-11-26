def reject_request_node(state):
    if state["is_request_valid"] is False:
        print("---------------------------------------------------------------------------------------")
        print("Request rejected during validation - ")
    elif state["manager_decision"] == "denied":
        print("---------------------------------------------------------------------------------------")
        print("Request rejected by manager - ")
    
    return state