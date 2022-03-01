from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    algorithm: str
    secret_key: str
    access_token_expires_in: int

    class Config:
        env_file = '.env'


settings = Settings()
