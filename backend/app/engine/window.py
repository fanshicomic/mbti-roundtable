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
        self.messages.append(message)
        if len(self.messages) > self.max_size:
            self.messages.pop(0)

    def push_high_priority(self, message: Message) -> None:
        """User interjection path: flags the message so impulse scoring reacts to it
        immediately, then enters the window like any other message (still subject to the cap)."""
        message.high_priority = True
        self.push(message)
