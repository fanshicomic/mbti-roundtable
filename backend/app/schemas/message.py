from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.schemas.types import MBTIType


class Message(BaseModel):
    speaker_mbti_type: MBTIType | None = None  # None for the user's own messages
    text: str
    is_user: bool = False
    high_priority: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
