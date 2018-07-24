import json

from flask import Flask, make_response, request

import bot

app = Flask(__name__)
pyBot = bot.Bot()
slack = pyBot.client


def _event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.

    Parameters
    ----------
    event_type : str
        type of event recieved from Slack
    slack_event : dict
        JSON response from a Slack reaction event

    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error

    """
    # ============= Reaction Added Events ============= #
    # If the user has added an emoji reaction to the onboarding message
    if event_type == "reaction_added":
        user_id = slack_event["event"]["user"]
        # Some messages aren't authored by "users," like those created by incoming webhooks.
        # reaction_added events related to these messages will not include an item_user.
        item_user_id = slack_event["event"].get("item_user")
        reaction = slack_event["event"]["reaction"]
        # only log others' poultry_leg reaction to a real user
        # if item_user_id and item_user_id != user_id and reaction == 'poultry_leg':
        if item_user_id and reaction == 'poultry_leg':      # test
            item = json.dumps(slack_event["event"]["item"], separators=(',', ':'))
            print(f'{user_id} ({reaction}) > {item_user_id} @({item})')
        return make_response("reaction logged", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


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
    # ============= Slack URL Verification ============ #
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    # ============ Slack Token Verification =========== #
    if pyBot.verification != slack_event.get("token"):
        message = f"Invalid Slack verification token: {slack_event['token']}\npyBot has: {pyBot.verification}\n\n"
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off Slack's automatic retries during
        # development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # ====== Process Incoming Events from Slack ======= #
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        # Then handle the event by event_type and have your bot respond
        return _event_handler(event_type, slack_event)

    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids you're looking for.",
                         404, {"X-Slack-No-Retry": 1})


def main():
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    main()
