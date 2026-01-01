import os, httpx
from database.db_connection import save_pending_request
from dotenv import load_dotenv

load_dotenv()

async def raise_license_allocation_incident(user_sys_id, software_name, description):
    instance = os.getenv("SERVICENOW_INSTANCE")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident"

    payload = {
        "short_description": f"Software installation request for {software_name}",
        "description": description,
        "caller_id": user_sys_id,
        "category": "software",
        "subcategory": "installation",
    }

    async with httpx.AsyncClient(auth=(username, password)) as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

    response.raise_for_status()
    return response.json()

async def license_allocation_node(state):
    requester_id = state["requester_id"]
    software_name = state["software_requested"]
    user_email = state["requester_email"]
    user_sys_id = state["requester_sys_id"]
    software_source = state["software_source"]
    software_type = state["software_type"]

    state["is_request_valid"] = True

    description = (
        f"User has requested installation of {software_name}. "
        f"The software is classified as {software_type} and is already approved. "
        f"The software is detected in {software_source} repository. "
        f"Software installation is requested by : {requester_id} - {user_email}"
    )

    state["incident_description"] = description

    auto_approved_condition = (
        (software_source == "workelevate" and software_type == "standard")
        or (
            software_source == "sam"
            and not state["is_software_restricted"]
            and not state["is_software_blacklisted"]
        )
    )

    if auto_approved_condition:
        incident = await raise_license_allocation_incident(
            user_sys_id,
            software_name,
            description
        )

        result = incident.get("result", {})
        state["incident_sys_id"] = result.get("sys_id", "")

        await save_pending_request(
            employee_id=requester_id,
            software=software_name,
            thread_id=state["thread_id"],
            status="approved_auto"
        )

        state["incident_raised"] = True
        state["is_request_valid"] = True

    return state