from pydantic import BaseSettings


class Config(BaseSettings):
    APP_PORT = 5000     # set os env GT_APP_PORT to overwrite
    DEBUG = False

    SLACK_CLIENT_ID: str = None
    SLACK_CLIENT_SECRET: str = None
    SLACK_VERIFICATION_TOKEN: str = None

    class Config:
        env_prefix = 'GT_'


CONFIG = Config()
