def human_intervention(state):
    print("\n--- HUMAN ESCALATION ---")
    print("Query:", state["query"])
    print("Context:", state["context"])

    response = input("Human agent response: ")

    state["response"] = response
    state["confidence"] = 1.0
    state["escalate"] = False

    return state