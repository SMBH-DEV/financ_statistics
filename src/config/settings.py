from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    LOGIN: str = Field(..., description='Логин, для подключение к сайту')
    PASSWORD: str = Field(..., description='Пароль, для подключение к сайту')
    URL: str = Field(..., description='Ссылка на сайт')
    
    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_DB: str = Field(default='financ_statistics')
    POSTGRES_HOST: str = Field(default='db')

    
    @property
    def db_uri(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}'
    
settings = Settings()

