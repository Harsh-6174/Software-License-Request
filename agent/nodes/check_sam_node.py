def check_sam_node(state):
    # Licence assets
    print("Requested software is not present in workelevate repo.")
    print("Checking if requested software is present in SAM.")

    if state["software_source"] == "sam":
        print("Software exists in SAM")
    else:
        print("Requested software is not present in SAM")
    return state