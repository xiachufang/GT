import os

from slackclient import SlackClient


class Bot:
    """ Instanciates a Bot object to handle Slack interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.client = SlackClient("")
