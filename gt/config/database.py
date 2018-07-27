from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    DB_NAME = "gt"
    DB_USER = "root"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_PASSWORD = ""
    DB_CHARSET = "utf8mb4"

    class Config:
        env_prefix = 'GT_'
