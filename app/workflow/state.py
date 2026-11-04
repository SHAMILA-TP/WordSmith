from typing import TypedDict

from app.llm.prompts.rewrite import RewriteContext
from app.schemas.rewrite import RewriteRequest


class RewriteState(TypedDict, total=False):
    """State of one rewrite run. Lives only for the length of the request.

    Each node returns only the keys it changes; LangGraph merges them in.
    """

    request: RewriteRequest
    context: RewriteContext
    text: str
