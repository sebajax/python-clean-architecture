from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "[Python Clean Architecture]"
    version: str = "v1.0.0"
    app_env: str = ""

    class Config:
        env_file = ".env"