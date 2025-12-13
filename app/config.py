from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    ENV: str = "local"

    # Hardcoded tokens for simplicity (can be loaded from env)
    TOKENS: dict = {
        "agent123": "agent",
        "admin123": "admin",
    }

    class Config:
        env_file = ".env"


settings = Settings()
