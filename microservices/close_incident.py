import os, httpx
from dotenv import load_dotenv

load_dotenv()

async def close_incident(incident_sys_id, payload):
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

    response.raise_for_status()
    print("Incident has been closed")
    return response.json()