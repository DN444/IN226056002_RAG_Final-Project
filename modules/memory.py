def update_memory(state):
    history = state.get("history", [])

    history.append({
        "user": state["query"],
        "bot": state["response"]
    })

    state["history"] = history
    return state