from langgraph.types import interrupt
from agent.llm.gemini_llm import run_llm
import json

async def employee_submit_request_node(state):
    user_message = interrupt(
        value = {
            "prompt" : "Describe your request in one message."
        }
    )

    prompt = f"""
    You will receive a user message requesting software license allocation.
    Extract the following fields exactly as stated by the user:

    - requester_id
    - software_requested
    - request_reason

    If the user did not provide a field, return an empty string for that field.
    Do not infer or assume anything.

    Return only a JSON dictionary with these three keys.

    User message:
    {user_message}
    """

    output = await run_llm(prompt)
    if output.startswith("```"):
        output = output.replace("```json","").replace("```","").strip()
    
    state["llm_response"] = output
    output = json.loads(output)

    requester_id = output.get("requester_id")
    software_requested = output.get("software_requested")
    request_reason = output.get("request_reason")

    if not requester_id:
        requester_id = interrupt(
            value = {
                "prompt": "You didn’t mentioned your Employee ID. Enter it now."
            }
        )
        # while not is_valid_requester_id(requester_id):
        #     requester_id = interrupt(
        #         value = {
        #             "prompt" : "Invalid Employee ID. Please try again."
        #         }
        #     )

    if not software_requested: 
        software_requested = interrupt( 
            value = { 
                "prompt" : "Which software do you need?" 
            } 
        ) 

    if not request_reason: 
        request_reason = interrupt( 
            value = { 
                "prompt" : "State the reason for requesting software." 
            } 
        )

    state["requester_id"] = requester_id.upper()
    state["software_requested"] = software_requested.lower()
    state["request_reason"] = request_reason.lower()

    return state