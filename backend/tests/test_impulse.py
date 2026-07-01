import random

from app.engine.impulse import compute_impulse, select_next_speaker
from app.schemas.character import Character
from app.schemas.message import Message
from app.schemas.types import MBTIType

NO_JITTER_RNG = random.Random()
NO_JITTER_RNG.uniform = lambda a, b: 0.0  # type: ignore[method-assign]


def test_recency_increases_impulse() -> None:
    candidate = Character(mbti_type=MBTIType.INFP)
    last_message = Message(speaker_mbti_type=MBTIType.ESTJ, text="whatever")

    recently_spoke_history = [Message(speaker_mbti_type=MBTIType.INFP, text="hi")]
    long_silent_history = [Message(speaker_mbti_type=MBTIType.ISTJ, text="hi")] * 5

    recent_score = compute_impulse(candidate, last_message, recently_spoke_history, rng=NO_JITTER_RNG)
    silent_score = compute_impulse(candidate, last_message, long_silent_history, rng=NO_JITTER_RNG)

    assert silent_score > recent_score


def test_direct_address_boosts_impulse() -> None:
    candidate = Character(mbti_type=MBTIType.INFP)
    history: list[Message] = []

    addressed = Message(speaker_mbti_type=MBTIType.ESTJ, text="hey INFP, explain yourself")
    ignored = Message(speaker_mbti_type=MBTIType.ESTJ, text="anyway, moving on")

    assert compute_impulse(candidate, addressed, history, rng=NO_JITTER_RNG) > compute_impulse(
        candidate, ignored, history, rng=NO_JITTER_RNG
    )


def test_high_priority_flag_counts_as_direct_address() -> None:
    candidate = Character(mbti_type=MBTIType.INFP)
    history: list[Message] = []
    high_priority = Message(speaker_mbti_type=MBTIType.ESTJ, text="anything", high_priority=True)
    normal = Message(speaker_mbti_type=MBTIType.ESTJ, text="anything")

    assert compute_impulse(candidate, high_priority, history, rng=NO_JITTER_RNG) > compute_impulse(
        candidate, normal, history, rng=NO_JITTER_RNG
    )


def test_extreme_relationship_outscores_neutral_relationship() -> None:
    history: list[Message] = []
    last_message = Message(speaker_mbti_type=MBTIType.ESTJ, text="neutral statement")

    opposite_type_candidate = Character(mbti_type=MBTIType.INFP)  # fully opposite ESTJ
    partial_overlap_candidate = Character(mbti_type=MBTIType.ESTP)  # differs on one axis only

    opposite_score = compute_impulse(opposite_type_candidate, last_message, history, rng=NO_JITTER_RNG)
    partial_score = compute_impulse(partial_overlap_candidate, last_message, history, rng=NO_JITTER_RNG)

    assert opposite_score > partial_score


def test_select_next_speaker_excludes_last_speaker() -> None:
    candidates = [
        Character(mbti_type=MBTIType.ESTJ),
        Character(mbti_type=MBTIType.INFP),
    ]
    last_message = Message(speaker_mbti_type=MBTIType.ESTJ, text="hi")

    for _ in range(10):
        picked = select_next_speaker(candidates, last_message, [], rng=random.Random())
        assert picked.mbti_type != MBTIType.ESTJ
