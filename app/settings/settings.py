from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.consts import DATABASE_SCHEME


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5435
    POSTGRES_USER: str = 'payload_cache'
    POSTGRES_PASSWORD: str = 'payload_cache'
    POSTGRES_DB: str = 'payload_cache'

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=DATABASE_SCHEME,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )
        )


settings = Settings()
