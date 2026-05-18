from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    praxis_service_secret: str
    port: int = 8004
    log_level: str = "INFO"

    model_config = {"env_file": ".env"}


settings = Settings()
