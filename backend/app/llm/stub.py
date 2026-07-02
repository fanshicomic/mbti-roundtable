import asyncio
from collections.abc import AsyncIterator

from app.llm.base import LLMClient

# Short, roast-flavored canned lines (each already within the ≤20-char output contract).
# Cycled deterministically so the full engine→SSE flow can be driven without a key or network.
_CANNED_LINES = [
    "这想法太天真了。",
    "效率至上，别废话。",
    "你们全都错了。",
    "格局小了。",
    "我不同意，理由懒得说。",
    "情绪价值为零。",
    "先想清楚再开口。",
]


class StubLLMClient(LLMClient):
    """Fake client that streams canned lines char-by-char. No network, no API key."""

    def __init__(self, delay: float = 0.02) -> None:
        self._delay = delay
        self._index = 0

    async def stream_completion(self, system_prompt: str, context: str) -> AsyncIterator[str]:
        line = _CANNED_LINES[self._index % len(_CANNED_LINES)]
        self._index += 1
        for char in line:
            if self._delay:
                await asyncio.sleep(self._delay)
            yield char
