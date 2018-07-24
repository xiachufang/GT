import json

from flask import Flask, make_response, request

import bot

app = Flask(__name__)
pyBot = bot.Bot()
slack = pyBot.client


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event handler helper function to route events
    to our Bot.
    """
    slack_event = json.loads(request.data)
    # to verify the url of our endpoint
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    # Slack Token Verification
    if pyBot.verification != slack_event.get("token"):
        message = f"Invalid Slack verification token: {slack_event['token']}\npyBot has: {pyBot.verification}\n\n"
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off Slack's automatic retries during
        # development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids you're looking for.",
                         404, {"X-Slack-No-Retry": 1})


def main():
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    main()
