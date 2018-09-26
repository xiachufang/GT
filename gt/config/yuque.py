from pydantic import BaseSettings


class YuqueConfig(BaseSettings):
    USERNAME = "user"
    PASSWORD = "pass"

    class Config:
        env_prefix = 'YUQUE_'
