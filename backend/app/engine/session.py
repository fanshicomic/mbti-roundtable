from app.engine.window import SlidingWindow
from app.schemas.character import Character
from app.schemas.session import SessionConfig, SessionState


class Session:
    """In-memory runtime state for one roundtable, keyed by session_id.

    Wraps the SessionState schema (the persisted/serializable snapshot) with the
    live SlidingWindow. Turn/time cap enforcement and user-message-limit checks
    live here, not in api/ handlers.
    """

    def __init__(self, session_id: str, config: SessionConfig, window_size: int) -> None:
        self.state = SessionState(session_id=session_id, config=config)
        self.window = SlidingWindow(scenario=config.scenario, max_size=window_size)

    @property
    def characters(self) -> list[Character]:
        return self.state.config.characters

    def is_over_turn_cap(self, turn_cap: int) -> bool:
        return self.state.turn_count >= turn_cap

    def can_user_speak(self, user_message_limit: int) -> bool:
        return self.state.user_message_count < user_message_limit
