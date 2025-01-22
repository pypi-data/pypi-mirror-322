from functools import lru_cache

from pydantic import BaseSettings

from .core import CredentialsManager


class Settings(BaseSettings):
    """
    Manages environment variables using pydantic.
    """

    @classmethod
    def from_credentials(cls, env_name="development"):
        """
        Dynamically loads environment variables from an encrypted .env.enc file.

        :param env_name: Environment name (e.g., development, production).
        :return: Settings instance.
        """
        credentials = CredentialsManager(env_name=env_name).decrypt_env()
        return cls(**credentials)


@lru_cache
def get_settings():
    return Settings()


envvault = get_settings()
