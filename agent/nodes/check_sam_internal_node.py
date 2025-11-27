def check_sam_internal_node(state):
    print("Checking if requested software is Restricted/Blacklisted/Allowed in SAM Internally.")

    if state["is_software_blacklisted"]:
        print("Requested software is blacklisted.")
        state["is_request_valid"] = False
        state["requires_manager_approval"] = False
        state["reason_rejection"] = "Requested software is blacklisted."
    elif state["is_software_restricted"]:
        print("Requested software is restricted. Requires manager approval.")
        state["is_request_valid"] = True
        state["requires_manager_approval"] = True
    else:
        print("Requested software can be installed and license can be allocated.")
        state["is_request_valid"] = True
        state["requires_manager_approval"] = False
    
    return state