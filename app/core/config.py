from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings using Pydantic BaseSettings."""

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 300
    SQLALCHEMY_DATABASE_URL: str = "sqlite:////app/abelton.db"



    class Config:
        """Settings configuration class."""

        case_sensitive = True


# Load the settings
settings = Settings()
