from typing import Any, Literal

import mercadopago  # type: ignore
from pydantic import (
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_PORT_EXT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    API_KEY: str

    # Services
    ITEMS_SERVICE_HTTP: bool = True
    ITEMS_SERVICE_HOST: str
    ITEMS_SERVICE_PORT: int | None = None
    ITEMS_SERVICE_API_KEY: str | None = None

    BUSINESS_SERVICE_HTTP: bool = True
    BUSINESS_SERVICE_HOST: str
    BUSINESS_SERVICE_PORT: int | None = None
    BUSINESS_SERVICE_API_KEY: str | None = None

    MERCADO_PAGO_PROD_ACCESS_TOKEN: str
    MERCADO_PAGO_NOTIFICATION_SECRET_KEY: str
    MERCADO_PAGO_NOTIFICATION_TEST_ID: str

    BOT_NAME: str

    # Testing
    POSTGRES_DB_TESTING: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def MERCADO_PAGO_SDK(self) -> Any:
        return mercadopago.SDK(self.MERCADO_PAGO_PROD_ACCESS_TOKEN)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def BOT_URL(self) -> Any:
        return f"https://t.me/{self.BOT_NAME}"


class TestSettings(Settings):
    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MultiHostUrl:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT_EXT,
            path=self.POSTGRES_DB_TESTING,
        )


settings = Settings()  # type: ignore[call-arg]

test_settings = TestSettings()  # type: ignore[call-arg]
