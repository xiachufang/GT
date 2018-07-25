from pydantic import BaseSettings


class Config(BaseSettings):
    APP_PORT = 5000     # set os env GT_APP_PORT to overwrite
    DEBUG = False

    SLACK_CLIENT_ID: str = None
    SLACK_CLIENT_SECRET: str = None
    SLACK_VERIFICATION_TOKEN: str = None
    SLACK_BOT_OAUTH_ACCESS_TOKEN: str = None

    DB_NAME = "gt"
    DB_USER = "root"
    DB_HOST = "gt-db-01"
    DB_PASSWORD = ""
    DB_CHARSET = "utf8mb4"

    class Config:
        env_prefix = 'GT_'


CONFIG = Config()
