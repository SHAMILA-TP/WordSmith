from fastapi import APIRouter, Depends
from langgraph.graph.state import CompiledStateGraph

from app.api.deps import get_rewrite_graph
from app.core.config import settings
from app.llm.prompts.rewrite import PROMPT_VERSION
from app.schemas.rewrite import RewriteRequest, RewriteResponse

router = APIRouter(prefix="/rewrite", tags=["rewrite"])


@router.post("", response_model=RewriteResponse)
def rewrite(
    request: RewriteRequest,
    graph: CompiledStateGraph = Depends(get_rewrite_graph),
):
    final_state = graph.invoke({"request": request})
    return RewriteResponse(
        text=final_state["text"],
        model=settings.llm_model,
        prompt_version=PROMPT_VERSION,
    )
