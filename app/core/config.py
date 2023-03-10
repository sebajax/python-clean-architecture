"""
core configuration for api
"""

from functools import lru_cache

from pydantic import BaseSettings, Field, Required, PostgresDsn


class Settings(BaseSettings):
    """
    class to represent the core settings for the api
    """
    # api libs env variables
    PROJECT_NAME: str = Field(default=Required, env="PROJECT_NAME")
    VERSION: str = "1.0.0"
    API_VERSION: str = "v1"
    API_PREFIX: str = f"/api/{API_VERSION}"
    QUERY_LIMIT: int = 50
    # database env variables
    DB_USER: str = Field(default=Required, env="DB_USER")
    DB_PASSWORD: str = Field(default=Required, env="DB_PASSWORD")
    DB_SERVER: str = Field(default=Required, env="DB_SERVER")
    DB_PORT: str = Field(default=Required, env="DB_PORT")
    DB_NAME: str = Field(default=Required, env="DB_NAME")
    # cache env variables
    CACHE_HOST: str = Field(default=None, env="CACHE_HOST")
    CACHE_PORT: int = Field(default=6379, env="CACHE_PORT")
    CACHE_DEFAULT_TTL: int = Field(default=2700, env="CACHE_DEFAULT_TTL")
    CACHE_PASSWORD: str = Field(default="sEcRet", env="CACHE_PASSWORD")
    # login jwt env variables
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SECRET_KEY: str = Field(default=Required, env='SECRET_KEY')
    ALGORITHM = "HS256"

    class Config:
        """
        class to represent the config for the api
        """
        env_file = ".env"

    def assemble_db_connection(self) -> str:
        """
        function that returns the postgres db connection string
        :return: connection string
        :rtype: str
        """
        url: str = PostgresDsn.build(
            scheme="postgresql",
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_SERVER,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME or ''}",
        )
        return url


@lru_cache
def get_settings() -> Settings:
    """
    function to generate settings instance and cache the setting using decorator
    :return: settings
    :rtype: Settings
    """
    return Settings()
