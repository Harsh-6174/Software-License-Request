def license_allocation_node(state):
    print("---------------------------------------------------------------------------")
    print("Software License allocated sucessfully!!!!")
    state["is_request_valid"] = True
    return state