def check_sam_node(state):
    print("Checking if requested software is present in SAM.")

    if state["software_source"] == "sam":
        print("Software exists in SAM")
    else:
        print("Software is not present in SAM")
    return state