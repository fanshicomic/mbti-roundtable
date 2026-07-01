from pydantic import BaseModel

from app.schemas.character import Character


class SessionConfig(BaseModel):
    """Submitted once at session creation: the scenario and the chosen roster."""

    scenario: str
    characters: list[Character]


class SessionState(BaseModel):
    session_id: str
    config: SessionConfig
    turn_count: int = 0
    user_message_count: int = 0
    ended: bool = False
