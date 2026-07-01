from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    seat_cap_free: int = 8
    seat_cap_unlocked: int = 16
    window_size: int = 8
    user_message_limit: int = 3
    output_max_words: int = 20
    session_turn_cap: int = 60
    session_time_cap_seconds: int = 20 * 60

    llm_provider: str = "stub"

    model_config = {"env_prefix": "MBTI_"}


settings = Settings()
