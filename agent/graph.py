from agent.state import State
from langgraph.graph import StateGraph, END

from agent.nodes.process_sources import process_sources
from agent.nodes.hybrid_retrieval import hybrid_retrieval
from agent.nodes.analyze_documents import analyze_documents
from agent.nodes.determine_format_specifications import determine_format_specifications
from agent.nodes.generate_content import generate_content

graph_builder = StateGraph(State)

# Add the nodes, including the new tool_node.
# graph_builder.add_node("human", human_node)
graph_builder.add_node("Process Sources", process_sources)
graph_builder.add_node("Hybrid Retrieval", hybrid_retrieval)
graph_builder.add_node("Analyze Documents", analyze_documents)
graph_builder.add_node("Determine Format Specifications", determine_format_specifications)
graph_builder.add_node("Generate Content", generate_content)


graph_builder.set_entry_point("Process Sources")

graph_builder.add_edge("Process Sources", "Hybrid Retrieval")
graph_builder.add_edge("Hybrid Retrieval", "Determine Format Specifications")
graph_builder.add_edge("Determine Format Specifications", "Analyze Documents")
graph_builder.add_edge("Analyze Documents", "Generate Content")


graph = graph_builder.compile()


if __name__ == "__main__":
    try:
        graph.get_graph().draw_mermaid_png()
    except Exception:
        pass