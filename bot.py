from slackclient import SlackClient

from config import CONFIG


# To remember which teams have authorized your app and what tokens are
# associated with each team, we can store this information in memory on
# as a global object. When your bot is out of development, it's best to
# save this in a more persistant memory store.
from storage import get_leg_leadboard

authed_teams = {}


class Bot:
    """ Instanciates a Bot object to handle Slack interactions."""
    def __init__(self):
        super(Bot, self).__init__()
        # When we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": CONFIG.SLACK_CLIENT_ID,
                      "client_secret": CONFIG.SLACK_CLIENT_SECRET,
                      # Scopes provide and limit permissions to what our app
                      # can access. It's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}

        self.verification = CONFIG.SLACK_VERIFICATION_TOKEN
        self.client = SlackClient(CONFIG.SLACK_BOT_OAUTH_ACCESS_TOKEN)

    # def auth(self, code):
    #     """
    #     Authenticate with OAuth and assign correct scopes.
    #     Save a dictionary of authed team information in memory on the bot
    #     object.
    #
    #     Parameters
    #     ----------
    #     code : str
    #         temporary authorization code sent by Slack to be exchanged for an
    #         OAuth token
    #
    #     """
    #     # After the user has authorized this app for use in their Slack team,
    #     # Slack returns a temporary authorization code that we'll exchange for
    #     # an OAuth token using the oauth.access endpoint
    #     auth_response = self.client.api_call(
    #                             "oauth.access",
    #                             client_id=self.oauth["client_id"],
    #                             client_secret=self.oauth["client_secret"],
    #                             code=code
    #                             )
    #     # To keep track of authorized teams and their associated OAuth tokens,
    #     # we will save the team ID and bot tokens to the global
    #     # authed_teams object
    #     team_id = auth_response["team_id"]
    #     print('>>> token:')
    #     print(auth_response["bot"]["bot_access_token"])
    #     authed_teams[team_id] = {"bot_token": auth_response["bot"]["bot_access_token"]}
    #     # Then we'll reconnect to the Slack Client with the correct team's bot token
    #     self.client = SlackClient(authed_teams[team_id]["bot_token"])

    def notify_being_added_poultry_leg(self, user_id, item_user_id):
        ret = self.client.api_call("im.open", user=item_user_id)
        dm_channel = ret["channel"]["id"]
        ret = self.client.api_call("chat.postMessage", channel=dm_channel,
                                   text=f'user({user_id}) add you a poultry leg')
        return ret["ok"]

    def get_user_data(self, user_id):
        ret = self.client.api_call("users.info", user=user_id)
        return ret["user"]

    def tell_leaderboard(self, channel):
        leg_leadboard_data = get_leg_leadboard()
        lines = ['=== 🍗 排行榜 🍗 ===']
        for idx, row in enumerate(leg_leadboard_data):
            user_name = self.get_user_data(row[0])['name']
            lines.append(f'{idx + 1}. {user_name} 🍗 x {row[1]}')
        ret = self.client.api_call("chat.postMessage", channel=channel, text='\n'.join(lines))
        return ret["ok"]
