import os, httpx
from database.db_connection import save_pending_request

async def raise_manager_approval_incident(user_sys_id, software_name, description):
    instance = os.getenv("SERVICENOW_INSTANCE")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident"

    payload = {
        "short_description": f"Manager approval required for {software_name}",
        "description": description,
        "caller_id": user_sys_id,
        "category": "software",
        "subcategory": "installation"
    }

    async with httpx.AsyncClient(auth=(username, password)) as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

    response.raise_for_status()
    return response.json()


async def create_manager_approval_incident_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    user_email = state["requester_email"]
    user_sys_id = state["requester_sys_id"]
    software_source = state["software_source"]
    software_type = state["software_type"]

    state["is_request_valid"] = True

    description = (
        f"User has requested installation of {software_name}. "
        f"The software is classified as {software_type} and requires manager approval. "
        f"The software is detected in {software_source} repository. "
        f"Software installation is requested by: {requester_id} - {user_email}"
    )

    state["incident_description"] = description

    needs_approval = (
        (software_source == "workelevate" and software_type == "licensed")
        or (
            software_source == "sam"
            and state["is_software_restricted"]
            and not state["is_software_blacklisted"]
        )
    )

    if needs_approval:
        if not state.get("incident_sys_id"):
            incident = await raise_manager_approval_incident(
                user_sys_id,
                software_name,
                description
            )

            result = incident.get("result", {})
            state["incident_sys_id"] = result.get("sys_id", "")
            print(f"Manager Approval Incident Created Sucessfully : {incident.get("result", {}).get("number", "invalid")}")

        await save_pending_request(
            employee_id=state["requester_id"],
            software=state["software_requested"],
            thread_id=state["thread_id"],
        )

    return state