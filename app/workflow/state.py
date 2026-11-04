import operator
import uuid
from typing import Annotated, TypedDict

from app.llm.prompts.rewrite import RewriteContext


class RewriteInput(TypedDict):
    """What callers pass to the graph."""

    brand_id: uuid.UUID
    property_id: uuid.UUID
    draft: str


class RewriteState(RewriteInput, total=False):
    """Internal state of the rewrite graph. Never returned to callers.

    Each node returns only the keys it changes; LangGraph merges them in.
    """

    # Filled by nodes, in order
    context: RewriteContext
    system_prompt: str
    user_prompt: str
    rewritten: str

    # Totals across all attempts. Annotated[..., operator.add] is a reducer:
    # a node returns just its own amount and LangGraph adds it to the total.
    attempts: Annotated[int, operator.add]
    input_tokens: Annotated[int, operator.add]
    output_tokens: Annotated[int, operator.add]
    latency_ms: Annotated[int, operator.add]


class RewriteOutput(TypedDict):
    """What the graph returns. Internal keys (prompts, guidelines) are left out."""

    rewritten: str
    attempts: int
    input_tokens: int
    output_tokens: int
    latency_ms: int
