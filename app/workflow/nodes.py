from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.errors import NotFoundError
from app.llm.client import LLMError
from app.llm.prompts.rewrite import (
    RewriteContext,
    build_system_prompt,
    build_user_prompt,
)
from app.models import Property
from app.workflow.deps import RewriteDeps
from app.workflow.state import RewriteState

Node = Callable[[RewriteState], RewriteState]


def make_load_context(deps: RewriteDeps) -> Node:
    def load_context(state: RewriteState) -> RewriteState:
        request = state["request"]
        # One query; the brand_id condition also checks the property belongs to the brand.
        query = (
            select(Property)
            .options(joinedload(Property.brand))
            .where(
                Property.id == request.property_id,
                Property.brand_id == request.brand_id,
            )
        )
        with deps.session_factory() as session:
            prop = session.scalars(query).one_or_none()
            if prop is None or not prop.is_active or not prop.brand.is_active:
                raise NotFoundError("Brand or property not found")
            brand = prop.brand
            context = RewriteContext(
                brand_name=brand.name,
                customer_term=brand.customer_term,
                property_name=prop.name,
                property_term=prop.property_term,
                brand_guidelines=brand.communication_guidelines,
                property_guidelines=prop.communication_guidelines,
            )
        return {"context": context}

    return load_context


def make_rewrite(deps: RewriteDeps) -> Node:
    def rewrite(state: RewriteState) -> RewriteState:
        result = deps.llm.generate(
            build_system_prompt(state["context"]),
            build_user_prompt(state["request"].draft),
        )
        if not result.text:
            raise LLMError("LLM returned an empty reply")
        return {"text": result.text}

    return rewrite
