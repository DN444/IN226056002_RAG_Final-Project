from typing import TypedDict, List, Dict


class GraphState(TypedDict, total=False):
    query: str
    intent: str
    context: List[str]
    response: str
    confidence: float
    escalate: bool
    history: List[Dict]