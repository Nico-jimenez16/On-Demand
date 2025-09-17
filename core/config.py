from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_description: str
    app_version: str
    app_port: int
    


    MONGODB_URL: str
    DATABASE_NAME: str
    COLLECTION_NAME: str
    
    CORS_ALLOW_ORIGINS: str
    CORS_ALLOW_CREDENTIALS: bool
    CORS_ALLOW_METHODS: str
    CORS_ALLOW_HEADERS: str

    class Config:
        env_file = ".env"

settings = Settings()