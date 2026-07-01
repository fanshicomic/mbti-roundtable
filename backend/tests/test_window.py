from app.engine.window import SlidingWindow
from app.schemas.message import Message


def make_message(text: str) -> Message:
    return Message(text=text)


def test_push_appends_within_cap() -> None:
    window = SlidingWindow(scenario="test scenario", max_size=3)
    window.push(make_message("a"))
    window.push(make_message("b"))
    assert [m.text for m in window.messages] == ["a", "b"]


def test_push_evicts_oldest_beyond_cap() -> None:
    window = SlidingWindow(scenario="test scenario", max_size=2)
    window.push(make_message("a"))
    window.push(make_message("b"))
    window.push(make_message("c"))
    assert [m.text for m in window.messages] == ["b", "c"]


def test_scenario_is_not_part_of_the_capped_queue() -> None:
    window = SlidingWindow(scenario="pinned premise", max_size=1)
    window.push(make_message("a"))
    window.push(make_message("b"))
    assert window.scenario == "pinned premise"
    assert [m.text for m in window.messages] == ["b"]


def test_push_high_priority_sets_flag() -> None:
    window = SlidingWindow(scenario="test scenario", max_size=5)
    message = make_message("user interjection")
    window.push_high_priority(message)
    assert window.messages[0].high_priority is True
