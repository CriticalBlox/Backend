from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_TITLE: str = "Api"
    API_VERSION: str = "1.0.0"
    RATE_LIMIT: int = 100
    DATABASE_URL: str
    DB_ECHO: bool = False

settings = Settings()