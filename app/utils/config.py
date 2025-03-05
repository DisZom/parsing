from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env")

    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5674

    RABBITMQ_DEFAULT_USER: str = "guest"
    RABBITMQ_DEFAULT_PASS: str = "guest"

    @property
    def BROKER_URI(self) -> str:
        return f"amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"

Config: Settings = Settings()
