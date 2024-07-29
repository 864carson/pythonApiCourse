from pydantic_settings import BaseSettings


# Manages settings and configurations.
class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_database: str = "ToDid"
    db_username: str = "postgres"
    db_password: str

    secret_key: str
    access_token_expiration: int = 240

    class Config:
        env_file = ".env"

settings = Settings()
