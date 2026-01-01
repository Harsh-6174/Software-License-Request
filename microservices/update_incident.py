import os, httpx

async def update_incident(incident_sys_id, payload):
    instance = os.getenv("SERVICENOW_INSTANCE")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident/{incident_sys_id}"

    async with httpx.AsyncClient(auth=(username, password)) as client:
        response = await client.patch(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

    if response.status_code >= 400:
        print("Failed to update incident")
        print(response.status_code, response.text)
        return None

    return response.json()