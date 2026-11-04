"""Thin wrapper around the chat model.

The rest of the app talks to LLMClient only. Swapping Ollama for another
provider means changing this file, nothing else.
"""

import logging
import time
from dataclasses import dataclass
from functools import lru_cache

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from app.core.config import settings

logger = logging.getLogger(__name__)

# Low temperature: rewriting should be stable, not creative.
DEFAULT_TEMPERATURE = 0.2


class LLMError(Exception):
    """Any failure talking to the model (down, timeout, unknown model, bad reply)."""


@dataclass(frozen=True)
class LLMResult:
    text: str
    input_tokens: int
    output_tokens: int
    latency_ms: int


class LLMClient:
    def __init__(
        self,
        model: str,
        base_url: str,
        timeout_seconds: float,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> None:
        self.model = model
        self._chat = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=temperature,
            client_kwargs={"timeout": timeout_seconds},
        )

    def generate(self, system_prompt: str, user_prompt: str) -> LLMResult:
        start = time.perf_counter()
        try:
            response = self._chat.invoke(
                [SystemMessage(system_prompt), HumanMessage(user_prompt)]
            )
        except Exception as exc:
            # Log the error only, never the prompts (they contain guest text).
            logger.warning(
                "LLM call failed: model=%s error=%s: %s",
                self.model,
                type(exc).__name__,
                exc,
            )
            raise LLMError(f"LLM call failed ({type(exc).__name__})") from exc
        latency_ms = round((time.perf_counter() - start) * 1000)

        if not isinstance(response.content, str):
            raise LLMError("LLM returned a non-text response")

        usage = response.usage_metadata or {}
        result = LLMResult(
            text=response.content.strip(),
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            latency_ms=latency_ms,
        )
        # Operational data only; never the prompt or the reply text.
        logger.info(
            "llm_call model=%s input_tokens=%d output_tokens=%d latency_ms=%d",
            self.model,
            result.input_tokens,
            result.output_tokens,
            result.latency_ms,
        )
        return result


@lru_cache(maxsize=1)
def get_llm_client() -> LLMClient:
    """One shared client per process (it holds an HTTP connection pool)."""
    return LLMClient(
        model=settings.llm_model,
        base_url=settings.ollama_base_url,
        timeout_seconds=settings.llm_timeout_seconds,
    )
