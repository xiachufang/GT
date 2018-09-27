import datetime
import hashlib
import json
import sys


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
    return this_monday - datetime.timedelta(days=7)


def trim_doc(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)
