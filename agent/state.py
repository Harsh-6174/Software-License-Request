from typing import TypedDict

class SoftwareRequestState(TypedDict):
    requester_id : str
    role: str
    thread_id: str
    requester_email: str
    requester_sys_id: str
    incident_sys_id: str
    incident_description: str
    is_requester_id_valid: bool
    software_requested : str
    request_reason : str
    is_request_valid : bool
    requires_manager_approval : bool
    software_source: str
    software_type: str
    security_approval: bool
    network_approval: bool
    sam_approval: bool
    is_software_restricted: bool
    is_software_blacklisted: bool
    manager_decision : str
    reason_rejection : str
    llm_response : str