from collections.abc import Iterator

from langgraph.graph.state import CompiledStateGraph
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.llm.client import get_llm_client
from app.workflow.deps import RewriteDeps
from app.workflow.graph import build_rewrite_graph


def get_db() -> Iterator[Session]:
    """One DB session per request; closed after the response is sent."""
    with SessionLocal() as session:
        yield session


def get_rewrite_graph() -> CompiledStateGraph:
    """The compiled rewrite graph. Equal deps hit the cache, so it is built once."""
    return build_rewrite_graph(
        RewriteDeps(session_factory=SessionLocal, llm=get_llm_client())
    )
