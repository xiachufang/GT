import logging
from typing import Any, Dict

from machine.plugins.base import MachineBasePlugin, Message
from machine.plugins.decorators import respond_to, process, listen_to
from slackclient.user import User
from texttable import Texttable

from ..store.storage import create_user_message_reaction_log, get_leg_leaderboard
from ..utils.helpers import hash_data, this_monday


def _create_user_message_reaction_log(to_user_id: str, from_user_id: str, msg_data: dict, reaction: str):
    # only log others' poultry_leg reaction to a real user
    if not to_user_id:
        return
    if from_user_id == to_user_id:
        return
    create_user_message_reaction_log(to_user_id=to_user_id, from_user_id=from_user_id,
                                     message_hash=hash_data(msg_data),
                                     reaction=reaction)


class ChickensPlugin(MachineBasePlugin):
    def __init__(self, settings, client, storage):
        super().__init__(settings, client, storage)
        self._bot_info = None

    def bot(self) -> dict:
        if not self._bot_info:
            self._bot_info = self.retrieve_bot_info()
        return self._bot_info

    # respond to anything but bot's join channel message
    @respond_to(r'^(?!has joined).*')
    def tell_leaderboard(self, msg: Message):
        logging.error(f'tell_leaderboard, {msg}')  # test for a while

        from_time = this_monday()
        leg_leaderboard_data = get_leg_leaderboard(from_time=from_time)

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
        msg.say(f'=== 🍗 本周排行榜 🍗 ===\n```{table.draw()}```')

    @listen_to(r'\<@(?P<to_user_id>.+)\>.*:poultry_leg:.*')
    def add_poultry_leg_by_mention(self, msg: Message, to_user_id: str):
        logging.error(f'add_poultry_leg_by_mention, {msg}')  # test for a while
        from_user_id = msg.sender.id
        msg_data = {
            'text': msg.text,
            'ts': msg.thread_ts,
        }

        if to_user_id == self.bot()['id']:
            return

        _create_user_message_reaction_log(from_user_id=from_user_id, to_user_id=to_user_id,
                                          msg_data=msg_data, reaction="poultry_leg")

    @process('reaction_added')
    def add_poultry_leg_by_reaction(self, event: Dict[str, Any]):
        logging.error(f'add_poultry_leg_by_reaction, {event}')  # test for a while
        user_id = event["user"]
        item_user_id = event.get("item_user", None)
        reaction = event["reaction"]

        if reaction != 'poultry_leg':
            return
        if item_user_id == self.bot()['id']:
            return

        _create_user_message_reaction_log(from_user_id=user_id, to_user_id=item_user_id,
                                          msg_data=event["item"], reaction=reaction)
        # self.send_dm(item_user_id, f'<@{user_id}> 热情的给你送了一个的鸡腿')
