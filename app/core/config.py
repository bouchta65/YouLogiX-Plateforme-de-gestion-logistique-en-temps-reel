from pydantic import BaseSettings, PostgresDsn


class Setting(BaseSettings):
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    POSTGRES_HOST:str="db"
    POSTGRES_PORT:int=5433
    DATABASE_URL:PostgresDsn = None 
    
    
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    class Config:
        env_file = ".env"
        
    @property
    def database_url(self):
        if self.database_url:
            return self.database_url
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Setting()