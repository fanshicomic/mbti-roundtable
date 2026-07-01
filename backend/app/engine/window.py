from app.schemas.message import Message


class SlidingWindow:
    """Per-session rolling context: pinned scenario + capped recent-message queue.

    Payload sent to the LLM is [persona prompt] + [pinned scenario] + [this window],
    per docs/PRD.md — the scenario is NOT part of the capped queue, so it never scrolls out.
    """

    def __init__(self, scenario: str, max_size: int) -> None:
        self.scenario = scenario
        self.max_size = max_size
        self.messages: list[Message] = []

    def push(self, message: Message) -> None:
        raise NotImplementedError

    def push_high_priority(self, message: Message) -> None:
        """User interjection path: bypasses normal ordering, injected for immediate effect."""
        raise NotImplementedError
