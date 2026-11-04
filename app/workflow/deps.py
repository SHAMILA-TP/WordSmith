from dataclasses import dataclass

from sqlalchemy.orm import Session, sessionmaker

from app.llm.client import LLMClient


@dataclass(frozen=True)
class RewriteDeps:
    """Long-lived collaborators the graph nodes need. Built once, shared."""

    session_factory: sessionmaker[Session]
    llm: LLMClient
