import datetime

import pymysql
from peewee import Model, MySQLDatabase, CharField, DateTimeField, IntegrityError, fn

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
    c_time = DateTimeField(default=datetime.datetime.now)


class UserMessageReactionLog(BaseModel):
    """
    user message reaction log
    prevent duplicate reaction, reaction stats
    """
    to_user_id = CharField()        # reaction to
    from_user_id = CharField()      # reaction from
    message_hash = CharField()
    reaction = CharField()
    c_time = DateTimeField(default=datetime.datetime.now)

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


def create_user_message_reaction_log(to_user_id, from_user_id, message_hash, reaction):
    try:
        UserMessageReactionLog.create(to_user_id=to_user_id, from_user_id=from_user_id,
                                      message_hash=message_hash, reaction=reaction)
    except IntegrityError:
        pass


def get_leg_leaderboard():
    ct_field = fn.COUNT(UserMessageReactionLog.id).alias('ct')
    query = UserMessageReactionLog.select(UserMessageReactionLog.to_user_id, ct_field).\
        where(UserMessageReactionLog.reaction == 'poultry_leg').\
        group_by(UserMessageReactionLog.to_user_id).order_by(ct_field.desc()).limit(20)
    ret = []
    for row_data in query:
        ret.append((row_data.to_user_id, row_data.ct))
    return ret


def create_tables():
    db.create_tables([EventLog, UserMessageReactionLog])
