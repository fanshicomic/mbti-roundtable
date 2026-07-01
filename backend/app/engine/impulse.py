from app.schemas.character import Character
from app.schemas.message import Message


def compute_impulse(candidate: Character, last_message: Message, history: list[Message]) -> float:
    """Speaking-impulse score: recency decay + direct-address boost + relationship_score + jitter.

    Not yet implemented — see docs/PRD.md "No moderator — impulse-driven speaker selection".
    """
    raise NotImplementedError


def select_next_speaker(candidates: list[Character], last_message: Message, history: list[Message]) -> Character:
    raise NotImplementedError
