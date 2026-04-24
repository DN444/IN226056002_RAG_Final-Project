from app.config import LLM


def generate_answer(state):
    history = state.get("history", [])

    prompt = f"""
    You are a customer support assistant.

    Conversation:
    {history}

    Context:
    {state['context']}

    Question:
    {state['query']}

    Rules:
    - Use only context
    - If unsure say "I don't know"
    """

    state["response"] = LLM.invoke(prompt).content
    return state