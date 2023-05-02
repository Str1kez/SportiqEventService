from os import environ

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    """
    Default configs for application.

    Usually, we have three environments: for development, testing and production.
    But in this situation, we only have standard settings for local development.
    """

    ENV: str = environ.get("ENV", "local")
    PATH_PREFIX: str = environ.get("PATH_PREFIX", "/api/v1")
    APP_HOST: str = environ.get("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "user_db")
    POSTGRES_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "user")
    POSTGRES_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "hackme")
    DB_CONNECT_RETRY: int = int(environ.get("DB_CONNECT_RETRY", 20))
    DB_POOL_SIZE: int = int(environ.get("DB_POOL_SIZE", 15))

    RABBITMQ_HOST: str = environ.get("RABBITMQ_HOST", "127.0.0.1")
    RABBITMQ_PORT: int = int(environ.get("RABBITMQ_PORT", 5672))
    RABBITMQ_DEFAULT_USER: str = environ.get("RABBITMQ_DEFAULT_USER", "rmuser")
    RABBITMQ_DEFAULT_PASS: str = environ.get("RABBITMQ_DEFAULT_PASS", "rmpassword")

    CACHE_URL: str = environ.get("CACHE_URL", "redis://localhost")

    HANDICAP_HOURS: int = int(environ.get("HANDICAP_HOURS", 1))
    EVENT_DURATION_MINUTES: int = int(environ.get("EVENT_DURATION_MINUTES", 15))

    @property
    def database_settings(self) -> dict:
        """
        Get all settings for connection with database.
        """
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def rabbitmq_settings(self) -> dict:
        """
        Get all settings for connection with rabbitmq.
        """
        return {
            "user": self.RABBITMQ_DEFAULT_USER,
            "password": self.RABBITMQ_DEFAULT_PASS,
            "host": self.RABBITMQ_HOST,
            "port": self.RABBITMQ_PORT,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def rabbitmq_uri(self) -> str:
        """
        Get uri for connection with rabbitmq.
        """
        return "amqp://{user}:{password}@{host}:{port}/".format(**self.rabbitmq_settings)

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
