from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATE_FORMAT: str

    # Twitter API credentials
    twitter_consumer_key: str
    twitter_consumer_secret: str
    twitter_access_token: str
    twitter_access_token_secret: str
    twitter_bearer_token: str

    LINKEDIN_CLIENT_ID: str
    LINKEDIN_CLIENT_SECRET: str
    LINKEDIN_ACCESS_TOKEN: str
    LINKEDIN_PERSON_URN: str
    LINKEDIN_ORGANIZATION_URN: str

    # GOOGLE credentials
    GOOGLE_API_KEY: str
    GOOGLE_MODEL: str

    class Config:
        env_file = "./.env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
