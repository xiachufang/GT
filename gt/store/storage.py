import datetime
from enum import Enum
from typing import List, Tuple, Optional

from peewee import Model, MySQLDatabase, CharField, DateTimeField, IntegrityError, fn, OperationalError, \
    __exception_wrapper__

from ..config import DB_CONFIG


class RetryOperationalError(object):

    def execute_sql(self, sql, params=None, commit=True):
        try:
            cursor = super(RetryOperationalError, self).execute_sql(
                sql, params, commit)
        except OperationalError:
            if not self.is_closed():
                self.close()
            with __exception_wrapper__:
                cursor = self.cursor()
                cursor.execute(sql, params or ())
                if commit and not self.in_transaction():
                    self.commit()
        return cursor


class MyRetryDB(RetryOperationalError, MySQLDatabase):
    pass


db = MyRetryDB(
    DB_CONFIG.DB_NAME,
    user=DB_CONFIG.DB_USER,
    host=DB_CONFIG.DB_HOST,
    port=DB_CONFIG.DB_PORT,
    password=DB_CONFIG.DB_PASSWORD,
    charset=DB_CONFIG.DB_CHARSET,
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


class AbstractReaction(str, Enum):
    """abstract reaction, not only the 'reaction' in slack"""
    REACTION_POULTRY_LEG = 'poultry_leg'
    MENTION_POULTRY_LEG = '@+poultry_leg'


class UserMessageReactionLog(BaseModel):
    """
    user message reaction log
    prevent duplicate reaction, reaction stats
    """
    to_user_id = CharField()  # reaction to
    from_user_id = CharField()  # reaction from
    message_hash = CharField()
    reaction = CharField()  # AbstractReaction
    c_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        indexes = (
            (('from_user_id', 'message_hash', 'reaction',), True),
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


def get_leaderboard(from_time: Optional[datetime.datetime] = None, to_time: Optional[datetime.datetime] = None)\
        -> List[Tuple[str, int]]:
    ct_field = fn.COUNT(UserMessageReactionLog.id).alias('ct')
    query = UserMessageReactionLog.select(UserMessageReactionLog.to_user_id, ct_field)
    if from_time:
        query = query.where(UserMessageReactionLog.c_time >= from_time)
    if to_time:
        query =query.where(UserMessageReactionLog.c_time <= to_time)
    query = query.group_by(UserMessageReactionLog.to_user_id).order_by(ct_field.desc()).limit(20)
    ret = []
    for row_data in query:
        ret.append((row_data.to_user_id, row_data.ct))
    return ret


def create_database():
    import pymysql
    conn = pymysql.connect(
        host=DB_CONFIG.DB_HOST,
        port=DB_CONFIG.DB_PORT,
        user=DB_CONFIG.DB_USER,
        passwd=DB_CONFIG.DB_PASSWORD,
    )
    conn.cursor().execute(
        f'CREATE DATABASE IF NOT EXISTS {DB_CONFIG.DB_NAME} '
        'DEFAULT CHARACTER SET utf8mb4 '
        'DEFAULT COLLATE utf8mb4_unicode_ci;',
    )


def create_tables():
    db.create_tables([EventLog, UserMessageReactionLog])
