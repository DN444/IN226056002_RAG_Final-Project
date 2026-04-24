from langgraph.graph import StateGraph
from app.state import GraphState

from modules.intent import classify_intent
from modules.evaluator import evaluate_answer
from modules.router import route_decision, route_agent
from modules.hitl import human_intervention
from modules.memory import update_memory
from modules.agents import billing_agent, support_agent


def build_graph(retriever):
    graph = StateGraph(GraphState)

    def retrieve_node(state):
        docs = retriever.retrieve(state["query"])
        state["context"] = docs
        return state

    # Nodes
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("intent", classify_intent)
    graph.add_node("billing", billing_agent)
    graph.add_node("support", support_agent)
    graph.add_node("evaluate", evaluate_answer)
    graph.add_node("hitl", human_intervention)
    graph.add_node("memory", update_memory)

    # Entry
    graph.set_entry_point("retrieve")

    # Flow
    graph.add_edge("retrieve", "intent")

    graph.add_conditional_edges(
        "intent",
        route_agent,
        {
            "billing": "billing",
            "support": "support"
        }
    )

    graph.add_edge("billing", "evaluate")
    graph.add_edge("support", "evaluate")

    graph.add_conditional_edges(
        "evaluate",
        route_decision,
        {
            "hitl": "hitl",
            "end": "memory"
        }
    )

    graph.add_edge("hitl", "memory")

    return graph.compile()