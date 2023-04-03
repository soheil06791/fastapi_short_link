from pydantic import BaseSettings

import os

file_path = os.path.split(os.path.abspath(__file__))[0]

class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str
    CLIENT_ORIGIN: str
    KEY_TOKEN: str
    DOMAIN: str

    class Config:
        env_file = f'{file_path}/.env'


settings = Settings()