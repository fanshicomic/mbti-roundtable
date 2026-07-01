from pydantic import BaseModel

from app.schemas.types import EmotionState, MBTIType


class Character(BaseModel):
    """A seated character. `custom_name` is None until the user renames it —
    display label is always derived (see label()), never overwrites mbti_type."""

    mbti_type: MBTIType
    custom_name: str | None = None
    emotion_state: EmotionState = EmotionState.NEUTRAL
    is_user: bool = False

    def label(self) -> str:
        if self.custom_name:
            return f"{self.custom_name} ({self.mbti_type.value})"
        return self.mbti_type.value
