from app.personas import CORE_DRIVERS, build_system_prompt
from app.schemas.character import Character
from app.schemas.types import MBTIType


def test_every_type_has_a_core_driver() -> None:
    assert set(CORE_DRIVERS) == set(MBTIType)


def test_every_type_builds_a_prompt_naming_its_type() -> None:
    for mbti in MBTIType:
        prompt = build_system_prompt(Character(mbti_type=mbti))
        assert mbti.value in prompt
        assert CORE_DRIVERS[mbti] in prompt


def test_renamed_character_uses_custom_name() -> None:
    prompt = build_system_prompt(Character(mbti_type=MBTIType.ESTJ, custom_name="老板"))
    assert "老板" in prompt
    assert "ESTJ" in prompt  # real type still present for correct roleplay


def test_unnamed_character_falls_back_to_type_as_name() -> None:
    prompt = build_system_prompt(Character(mbti_type=MBTIType.INFP))
    assert "「INFP」" in prompt


def test_empty_custom_name_falls_back_to_type() -> None:
    prompt = build_system_prompt(Character(mbti_type=MBTIType.INFP, custom_name=""))
    assert "「INFP」" in prompt
