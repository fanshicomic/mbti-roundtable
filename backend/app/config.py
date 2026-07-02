from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    seat_cap_free: int = 8
    seat_cap_unlocked: int = 16
    window_size: int = 8
    user_message_limit: int = 3
    output_max_words: int = 20
    session_turn_cap: int = 60
    session_time_cap_seconds: int = 20 * 60

    llm_provider: str = "stub"  # "stub" | "deepseek"
    llm_max_tokens: int = 64  # cost guard; the real ≤20-word contract is enforced in moderation/

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-chat"

    model_config = {"env_prefix": "MBTI_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
