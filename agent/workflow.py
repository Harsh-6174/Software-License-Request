from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from agent.state import SoftwareRequestState
from agent.nodes.employee_submit_request_node import employee_submit_request_node
from agent.nodes.validate_request_node import validate_request_node
from agent.nodes.manager_approval_node import manager_approval_node
from agent.nodes.reject_request_node import reject_request_node
from agent.nodes.license_allocation_node import license_allocation_node
from agent.nodes.notify_user_node import notify_user_node
from agent.nodes.logging_process_node import logging_process_node



def build_graph():
    def route_after_validate_request(state):
        if state["is_request_valid"] and state["requires_manager_approval"]:
            return "manager_approval"
        elif state["is_request_valid"] and state["requires_manager_approval"] is False:
            return "license_allocation"
        elif state["is_request_valid"] is False:
            return "reject_request"
        else:
            return "reject_request"

    def route_after_manager_approval(state):
        if state["manager_decision"] == "approved":
            return "license_allocation"
        else:
            return "reject_request"

    graph = StateGraph(SoftwareRequestState)

    graph.add_node("employee_submit_request", employee_submit_request_node)
    graph.add_node("validate_request", validate_request_node)
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
        route_after_validate_request,
        {
            "reject_request": "reject_request",
            "manager_approval": "manager_approval",
            "license_allocation": "license_allocation"
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
