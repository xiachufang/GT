import logging
from typing import Any, Dict

from machine.plugins.base import MachineBasePlugin, Message
from machine.plugins.decorators import respond_to, process
from slackclient.user import User
from texttable import Texttable

from ..store.storage import create_user_message_reaction_log, get_leg_leaderboard
from ..utils.helpers import hash_data


class ChickensPlugin(MachineBasePlugin):
    def __init__(self, settings, client, storage):
        super().__init__(settings, client, storage)
        self._bot_info = None

    def bot(self) -> dict:
        if not self._bot_info:
            self._bot_info = self.retrieve_bot_info()
        return self._bot_info

    # respond to anything but bot's join channel message
    @respond_to(r'^(?!has joined the channel).*')
    def tell_leaderboard(self, msg: Message):
        logging.error(f'*, {msg}')  # test for a while
        leg_leaderboard_data = get_leg_leaderboard()

        table = Texttable()
        table.set_cols_align(["l", "r", "l"])
        table.add_row(['Index', 'Name', '🍗'])
        users = self.users

        for idx, (user_id, t) in enumerate(leg_leaderboard_data):
            user: User = users.get(user_id)
            user_name = user_id
            if user:
                user_name = user.name
            table.add_row([idx + 1, user_name, f'🍗 x {t}'])

        msg.say(f'=== 🍗 排行榜 🍗 ===\n```{table.draw()}```')

    @process('reaction_added')
    def reaction_to(self, event: Dict[str, Any]):
        logging.error(f'reaction_added, {event}')  # test for a while
        user_id = event["user"]
        item_user_id = event.get("item_user", None)
        reaction = event["reaction"]

        # only log others' poultry_leg reaction to a real user
        if not item_user_id:
            return
        if item_user_id == self.bot()['id']:
            return
        if reaction != 'poultry_leg':
            return
        if item_user_id == user_id:
            return

        create_user_message_reaction_log(to_user_id=item_user_id, from_user_id=user_id,
                                         message_hash=hash_data(event["item"]),
                                         reaction=reaction)
        # self.send_dm(item_user_id, f'<@{user_id}> 热情的给你送了一个的鸡腿')
