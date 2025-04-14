from agent.state import State
from langgraph.graph import StateGraph, END

from agent.nodes.process_sources import process_sources
from agent.nodes.hybrid_retrieval import hybrid_retrieval
from agent.nodes.analyze_documents import analyze_documents
from agent.nodes.determine_format_specifications import determine_format_specifications
from agent.nodes.router import router
from agent.nodes.generate_content import generate_content
from agent.nodes.refine import refine
from agent.nodes.query import query
from agent.nodes.follow_up import follow_up

def decide_route(state: State):
    route = state.get("route", "Query")

    if "generate" in route.lower():
        route = "Generate"
    elif "refine" in route.lower():
        route = "Refine"
    if "query" in route.lower():
        route = "Query"

    print("Next Route:", route)
    state["route"] = route

    return route

graph_builder = StateGraph(State)

graph_builder.add_node("Process Sources", process_sources)
graph_builder.add_node("Hybrid Retrieval", hybrid_retrieval)
graph_builder.add_node("Analyze Documents", analyze_documents)
graph_builder.add_node("Determine Format Specifications", determine_format_specifications)
graph_builder.add_node("Router", router)
graph_builder.add_node("Generate", generate_content)
graph_builder.add_node("Refine", refine) 
graph_builder.add_node("Query", query) 
graph_builder.add_node("Follow Up", follow_up)

graph_builder.add_edge("Process Sources", "Hybrid Retrieval")
graph_builder.add_edge("Hybrid Retrieval", "Determine Format Specifications")
graph_builder.add_edge("Determine Format Specifications", "Analyze Documents")
graph_builder.add_edge("Analyze Documents", "Router")

graph_builder.add_conditional_edges("Router", decide_route, {val : val for val in {"Generate", "Refine", "Query"}})

graph_builder.add_edge("Generate", "Follow Up")
graph_builder.add_edge("Refine", "Follow Up")
graph_builder.add_edge("Query", END)
graph_builder.add_edge("Follow Up", END)

graph_builder.set_entry_point("Process Sources")

graph = graph_builder.compile()

# print(graph.get_graph().draw_mermaid_png())