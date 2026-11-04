from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from app.workflow.deps import RewriteDeps
from app.workflow.nodes import make_load_context, make_rewrite
from app.workflow.state import RewriteState


@lru_cache(maxsize=8)
def build_rewrite_graph(deps: RewriteDeps) -> CompiledStateGraph:
    """Build and compile the graph once per deps object.

    No checkpointer: the state lives only for one request and is not saved.
    """
    graph = StateGraph(RewriteState)
    graph.add_node("load_context", make_load_context(deps))
    graph.add_node("rewrite", make_rewrite(deps))
    graph.add_edge(START, "load_context")
    graph.add_edge("load_context", "rewrite")
    graph.add_edge("rewrite", END)
    return graph.compile()
