import hashlib
import json


def hash_data(data: dict) -> str:
    s = json_compact_dumps(data)
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def json_compact_dumps(data: dict) -> str:
    return json.dumps(data, separators=(',', ':'))


def json_loads(s: str) -> dict:
    return json.load(s)
