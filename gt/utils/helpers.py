import datetime
import hashlib
import json


def hash_data(data: dict) -> str:
    s = json_compact_dumps(data)
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def json_compact_dumps(data: dict) -> str:
    return json.dumps(data, separators=(',', ':'))


def json_loads(s: str) -> dict:
    return json.load(s)


def get_this_monday():
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)
    this_monday = today - datetime.timedelta(now.weekday())
    return this_monday

def get_prev_monday():
    this_monday = get_this_monday()
    return this_monday - datetime.timedelta(days=-1)
