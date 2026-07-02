from abc import ABC, abstractmethod
from collections.abc import AsyncIterator


class LLMClient(ABC):
    """Provider-agnostic streaming completion interface.

    Nothing outside this package should know which provider is in use —
    swapping DeepSeek/OpenAI/Claude must not touch engine/ or personas/.
    Implementations are async generators yielding text chunks as they arrive.
    """

    @abstractmethod
    def stream_completion(self, system_prompt: str, context: str) -> AsyncIterator[str]:
        ...
