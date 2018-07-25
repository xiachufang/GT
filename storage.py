import datetime

import pymysql
from peewee import Model, MySQLDatabase, CharField, DateTimeField, Tuple

from config import CONFIG

db = MySQLDatabase(
        CONFIG.DB_NAME,
        user=CONFIG.DB_USER,
        host=CONFIG.DB_HOST,
        password=CONFIG.DB_PASSWORD,
        charset=CONFIG.DB_CHARSET,
    )

conn = pymysql.connect(
    host=CONFIG.DB_HOST,
    user=CONFIG.DB_USER,
    passwd=CONFIG.DB_PASSWORD,
)


def create_database():
    conn.cursor().execute(
        f'CREATE DATABASE IF NOT EXISTS {CONFIG.DB_NAME} '
        'DEFAULT CHARACTER SET utf8mb4 '
        'DEFAULT COLLATE utf8mb4_unicode_ci;',
    )


class BaseModel(Model):
    class Meta:
        database = db



class EventLog(BaseModel):
    """
    slack event log
    prevent duplicate processing
    """
    event_hash = CharField(index=True)
    c_time = DateTimeField(default=datetime.datetime.now())


class UserMessageReactionLog(BaseModel):
    """
    user message reaction log
    prevent duplicate reaction, reaction stats
    """
    to_user_id = CharField()        # reaction to
    from_user_id = CharField()      # reaction from
    message_hash = CharField()
    reaction = CharField()
    c_time = DateTimeField(default=datetime.datetime.now())

    class Meta:
        indexes = (
            (('from_user_id', 'message_hash', 'reaction', ), True),
            (('reaction', 'c_time', 'to_user_id',), False),
        )


def get_or_create_event_log(event_hash: str):
    """
    :param event_hash: hash of slack event data
    :return: event_log, created
    """
    return EventLog.get_or_create(event_hash=event_hash)


def create_tables():
    db.create_tables([EventLog,])
