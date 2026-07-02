from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from app.config import settings
from app.llm.base import LLMClient


class DeepSeekClient(LLMClient):
    """DeepSeek via its OpenAI-compatible chat/completions endpoint.

    system_prompt -> the "system" message, context (rendered scenario + window) -> the "user" message.
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
    ) -> None:
        self._client = AsyncOpenAI(
            api_key=api_key or settings.deepseek_api_key,
            base_url=base_url or settings.deepseek_base_url,
        )
        self._model = model or settings.llm_model
        self._max_tokens = max_tokens or settings.llm_max_tokens

    async def stream_completion(self, system_prompt: str, context: str) -> AsyncIterator[str]:
        stream = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ],
            max_tokens=self._max_tokens,
            stream=True,
        )
        async for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
