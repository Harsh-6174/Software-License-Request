import os, requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

def close_incident(incident_sys_id, payload):
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

    print(f"Incident has been closed")
    return response.json()