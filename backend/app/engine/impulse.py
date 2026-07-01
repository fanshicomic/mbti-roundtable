import random

from app.engine.relationships import relationship_score
from app.schemas.character import Character
from app.schemas.message import Message

RECENCY_WEIGHT = 0.2
RECENCY_CAP_TURNS = 5
DIRECT_ADDRESS_BOOST = 1.0
RELATIONSHIP_WEIGHT = 0.5
JITTER_MAX = 0.3
MIN_SELECTION_WEIGHT = 0.01


def _turns_since_last_spoke(candidate: Character, history: list[Message]) -> int:
    for turns_ago, message in enumerate(reversed(history), start=1):
        if message.speaker_mbti_type == candidate.mbti_type:
            return turns_ago - 1
    return len(history)


def _is_directly_addressed(candidate: Character, message: Message) -> bool:
    return message.high_priority or candidate.mbti_type.value in message.text or (
        candidate.custom_name is not None and candidate.custom_name in message.text
    )


def compute_impulse(
    candidate: Character,
    last_message: Message,
    history: list[Message],
    rng: random.Random | None = None,
) -> float:
    """Speaking-impulse score: recency decay + direct-address boost + relationship pull + jitter.

    Relationship contribution uses the *magnitude* of relationship_score, not its sign: both
    strong friction (roast-bait) and strong affinity (jump in to agree) drive engagement more
    than a neutral relationship does. See docs/PRD.md "No moderator — impulse-driven speaker
    selection".
    """
    rng = rng or random.Random()

    recency_term = min(_turns_since_last_spoke(candidate, history), RECENCY_CAP_TURNS) * RECENCY_WEIGHT
    address_term = DIRECT_ADDRESS_BOOST if _is_directly_addressed(candidate, last_message) else 0.0

    relationship_term = 0.0
    if last_message.speaker_mbti_type is not None:
        raw_relationship = relationship_score(last_message.speaker_mbti_type, candidate.mbti_type)
        relationship_term = abs(raw_relationship) * RELATIONSHIP_WEIGHT

    jitter_term = rng.uniform(0, JITTER_MAX)

    return recency_term + address_term + relationship_term + jitter_term


def select_next_speaker(
    candidates: list[Character],
    last_message: Message,
    history: list[Message],
    rng: random.Random | None = None,
) -> Character:
    rng = rng or random.Random()

    eligible = [c for c in candidates if c.mbti_type != last_message.speaker_mbti_type]
    if not eligible:
        eligible = candidates

    weights = [max(compute_impulse(c, last_message, history, rng), MIN_SELECTION_WEIGHT) for c in eligible]
    return rng.choices(eligible, weights=weights, k=1)[0]
