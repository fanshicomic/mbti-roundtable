from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class LLMClient(ABC):
    """Provider-agnostic streaming completion interface.

    Nothing outside this package should know which provider is in use —
    swapping DeepSeek/OpenAI/Claude must not touch engine/ or personas/.
    """

    @abstractmethod
    async def stream_completion(self, system_prompt: str, context: str) -> AsyncIterator[str]:
        """Yields text chunks as they arrive from the provider."""
        raise NotImplementedError
        yield ""  # pragma: no cover - makes this an async generator for subclasses to override
