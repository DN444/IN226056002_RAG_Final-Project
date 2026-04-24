def route_agent(state):
    intent = state.get("intent", "")

    if "billing" in intent:
        return "billing"

    return "support"


def route_decision(state):
    confidence = state.get("confidence", 0)
    context = state.get("context", [])

    if confidence < 0.6 or len(context) == 0:
        state["escalate"] = True
        return "hitl"

    state["escalate"] = False
    return "end"