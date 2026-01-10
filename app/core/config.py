from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Setting(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: Optional[str] = None

    model_config = ConfigDict(env_file=".env")
        
    @property
    def database_url(self):
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Setting()