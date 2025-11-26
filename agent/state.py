from typing import TypedDict

class SoftwareRequestState(TypedDict):
    requester_id : str
    software_requested : str
    request_reason : str
    is_request_valid : bool
    requires_manager_approval : bool
    software_source: str
    software_type: str
    is_software_restricted: bool
    is_software_blacklisted: bool
    reason_rejection : str
    manager_decision : str
    llm_response : str