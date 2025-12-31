import os, requests
from requests.auth import HTTPBasicAuth

def update_incident(incident_sys_id, payload):
    instance = os.getenv("SERVICENOW_INSTANCE")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance}/api/now/table/incident/{incident_sys_id}"

    response = requests.patch(
        url,
        json=payload,
        auth=HTTPBasicAuth(username,password),
        headers={"Content-Type": "application/json"}
    )

    if not response.ok:
        print("Failed to update incident")
        print(response.status_code, response.text)
        return None

    return response.json()