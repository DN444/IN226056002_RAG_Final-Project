from app.config import LLM


def classify_intent(state):
    prompt = f"""
    Classify intent into:
    faq, troubleshooting, billing, complex

    Query: {state['query']}
    """

    state["intent"] = LLM.invoke(prompt).content.strip().lower()
    return state