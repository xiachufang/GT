# import logging
# LOGLEVEL = logging.DEBUG
SLACK_API_TOKEN = 'xoxb-324216556786-9oEmtrZeuHtGk9JB8EmXEhz4'
HTTP_PROXY = 'socks5://127.0.0.1:1086'
HTTPS_PROXY = 'socks5://127.0.0.1:1086'
PLUGINS = [
    'machine.plugins.builtin.general.PingPongPlugin',
    'machine.plugins.builtin.general.HelloPlugin',
    'machine.plugins.builtin.debug.EventLoggerPlugin',
    'gt.plugins.chickens.ChickensPlugin',
]
