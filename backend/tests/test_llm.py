import asyncio

import pytest

from app import config
from app.llm import get_llm_client
from app.llm.base import LLMClient
from app.llm.stub import StubLLMClient


def _collect(client: LLMClient) -> list[str]:
    async def run() -> list[str]:
        return [chunk async for chunk in client.stream_completion("system", "context")]

    return asyncio.run(run())


def test_stub_streams_single_char_chunks() -> None:
    chunks = _collect(StubLLMClient(delay=0))
    assert chunks
    assert all(len(c) == 1 for c in chunks)


def test_stub_cycles_through_lines() -> None:
    client = StubLLMClient(delay=0)
    first = "".join(_collect(client))
    second = "".join(_collect(client))
    assert first != second  # advances to the next canned line


def test_factory_returns_stub_by_default() -> None:
    client = get_llm_client()
    assert isinstance(client, StubLLMClient)


def test_factory_dispatches_deepseek(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "llm_provider", "deepseek")
    monkeypatch.setattr(config.settings, "deepseek_api_key", "sk-test")
    from app.llm.deepseek import DeepSeekClient

    assert isinstance(get_llm_client(), DeepSeekClient)


def test_factory_unknown_provider_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(config.settings, "llm_provider", "nope")
    with pytest.raises(ValueError):
        get_llm_client()
