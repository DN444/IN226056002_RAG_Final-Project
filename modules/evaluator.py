from app.config import LLM


def evaluate_answer(state):
    prompt = f"""
    Evaluate answer quality from 0 to 1.

    Context: {state['context']}
    Answer: {state['response']}

    Return only a number.
    """

    try:
        state["confidence"] = float(LLM.invoke(prompt).content.strip())
    except:
        state["confidence"] = 0.5
    state["escalate"] = False

    return state