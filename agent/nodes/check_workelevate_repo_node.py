import json
from microservices.software_name_match import resolve_software_name

with open("microservices/softwares.json") as f:
    softwares = json.load(f)

def check_workelevate_repo_node(state):
    req = state["software_requested"].lower()
    best_match, software_obj = resolve_software_name(req)

    print(f"Best software match - {best_match}")

    state["software_requested"] = best_match
    state["software_type"] = software_obj["license_type"]
    if state["software_type"] == "licensed":
        state["requires_manager_approval"] = True
    state["is_software_restricted"] = software_obj["is_restricted"]
    state["is_software_blacklisted"] = software_obj["is_blacklisted"]
    state["software_source"] = software_obj["source"]

    return state