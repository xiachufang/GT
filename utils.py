import hashlib
import json


def hash_data(data: dict) -> str:
    s = json.dumps(data, separators=(',', ':'))
    return hashlib.md5(s.encode('utf-8')).hexdigest()
