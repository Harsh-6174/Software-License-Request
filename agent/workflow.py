from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from agent.state import SoftwareRequestState
from agent.nodes.employee_submit_request_node import employee_submit_request_node
from agent.nodes.validate_request_node import validate_request_node
from agent.nodes.check_workelevate_repo_node import check_workelevate_repo_node
from agent.nodes.check_sam_node import check_sam_node
from agent.nodes.check_sam_internal_node import check_sam_internal_node
from agent.nodes.check_external_node import check_external_node
from agent.nodes.manager_approval_node import manager_approval_node
from agent.nodes.reject_request_node import reject_request_node
from agent.nodes.license_allocation_node import license_allocation_node
from agent.nodes.notify_user_node import notify_user_node
from agent.nodes.logging_process_node import logging_process_node



def build_graph():
    def route_after_validation(state):
        if state["is_request_valid"] is False:
            return "notify_user"
        else:
            return "check_workelevate_repo"

    def route_after_check_workelevate_repo(state):
        if state["software_source"] != "workelevate":
            return "check_sam"
        
        if state["software_type"] == "standard":
            return "license_allocation"
        else:
            return "manager_approval"
        
    def route_after_check_sam(state):
        if state["software_source"] == "sam":
            return "check_sam_internal"
        else:
            return "check_external"
    
    def route_after_check_sam_internal(state):
        if state["is_software_blacklisted"]:
            return "reject_request"
        if state["is_software_restricted"]:
            return "manager_approval"
        return "license_allocation"
    
    def route_after_check_external(state):
        if state["is_software_blacklisted"]:
            return "reject_request"
        else:
            return "manager_approval"

    def route_after_manager_approval(state):
        if state["manager_decision"] == "approved":
            return "license_allocation"
        else:
            return "reject_request"

    graph = StateGraph(SoftwareRequestState)

    graph.add_node("employee_submit_request", employee_submit_request_node)
    graph.add_node("validate_request", validate_request_node)
    graph.add_node("check_workelevate_repo", check_workelevate_repo_node)
    graph.add_node("check_sam", check_sam_node)
    graph.add_node("check_sam_internal", check_sam_internal_node)
    graph.add_node("check_external", check_external_node)
    graph.add_node("manager_approval", manager_approval_node)
    graph.add_node("reject_request", reject_request_node)
    graph.add_node("license_allocation", license_allocation_node)
    graph.add_node("notify_user", notify_user_node)
    graph.add_node("logging_process", logging_process_node)

    graph.add_edge(START, "employee_submit_request")
    graph.add_edge("employee_submit_request", "validate_request")
    graph.add_edge("reject_request", "notify_user")
    graph.add_edge("license_allocation", "notify_user")
    graph.add_edge("notify_user", "logging_process")

    graph.add_conditional_edges(
        "validate_request",
        route_after_validation,
        {
            "notify_user": "notify_user",
            "check_workelevate_repo": "check_workelevate_repo"
        }
    )

    graph.add_conditional_edges(
        "check_workelevate_repo",
        route_after_check_workelevate_repo,
        {
            "check_sam": "check_sam",
            "license_allocation": "license_allocation",
            "manager_approval": "manager_approval"
        }
    )

    graph.add_conditional_edges(
        "check_sam",
        route_after_check_sam,
        {
            "check_sam_internal": "check_sam_internal",
            "check_external": "check_external"
        }
    )

    graph.add_conditional_edges(
        "check_sam_internal",
        route_after_check_sam_internal,
        {
            "manager_approval": "manager_approval",
            "reject_request": "reject_request",
            "license_allocation": "license_allocation"
        }
    )

    graph.add_conditional_edges(
        "check_external",
        route_after_check_external,
        {
            "reject_request": "reject_request",
            "manager_approval": "manager_approval"
        }
    )

    graph.add_conditional_edges(
        "manager_approval",
        route_after_manager_approval,
        {
            "reject_request": "reject_request",
            "license_allocation": "license_allocation"
        }
    )

    graph.add_edge("logging_process", END)

    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)

    return app