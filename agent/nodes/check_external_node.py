def check_external_node(state):
    print("Requested software is not present in Workelevate repo or SAM.")

    if state["is_software_blacklisted"]:
        print("Requested software is blacklisted.")
        state["is_request_valid"] = False
        state["reason_rejection"] = "Requested software is blacklisted and not present in Workelevate repo or SAM."
    else:
        print("Requested software requires manager approval as it is not present in the organization's repo.")
        state["is_request_valid"] = True
        state["requires_manager_approval"] = True
    return state