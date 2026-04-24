from app.config import LLM


def billing_agent(state):
    prompt = f"""
    You are a BILLING SUPPORT agent.

    Context:
    {state['context']}

    Question:
    {state['query']}

    Answer specifically about:
    - payments
    - refunds
    - invoices
    """

    state["response"] = LLM.invoke(prompt).content
    return state


def support_agent(state):
    prompt = f"""
    You are a GENERAL CUSTOMER SUPPORT agent.

    Context:
    {state['context']}

    Question:
    {state['query']}

    Answer specifically about:
    - delivery
    - returns
    - product issues
    - account problems
    """

    state["response"] = LLM.invoke(prompt).content
    return state