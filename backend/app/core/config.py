from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Gym Buddy API"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "gym_buddy"
    cors_origins: list[str] = ["http://localhost:3000"]
    use_in_memory_store: bool = True
    session_cookie_name: str = "gym_buddy_session"
    session_ttl_days: int = 14

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
