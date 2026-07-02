from app.config import settings
from app.llm.base import LLMClient
from app.llm.stub import StubLLMClient


def get_llm_client() -> LLMClient:
    """Select the streaming client from config. DeepSeek is imported lazily so the
    stub/test paths never require the openai package or an API key at import time."""
    provider = settings.llm_provider
    if provider == "stub":
        return StubLLMClient()
    if provider == "deepseek":
        from app.llm.deepseek import DeepSeekClient

        return DeepSeekClient()
    raise ValueError(f"Unknown LLM provider: {provider!r}")


__all__ = ["LLMClient", "StubLLMClient", "get_llm_client"]
