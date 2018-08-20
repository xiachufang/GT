import logging
from typing import Any, Dict

from machine.plugins.base import MachineBasePlugin, Message
from machine.plugins.decorators import respond_to, process, listen_to, schedule
from slackclient.user import User
from texttable import Texttable

from ..store.storage import create_user_message_reaction_log, get_leaderboard, AbstractReaction
from ..utils.helpers import hash_data, get_this_monday, get_prev_monday


def _create_user_message_reaction_log(to_user_id: str, from_user_id: str, msg_data: dict, reaction: str):
    # only log others' poultry_leg reaction to a real user
    if not to_user_id:
        return
    if from_user_id == to_user_id:
        return
    create_user_message_reaction_log(to_user_id=to_user_id, from_user_id=from_user_id,
                                     message_hash=hash_data(msg_data),
                                     reaction=reaction)


def _get_leaderboard_msg_text(title, users, from_time=None, to_time=None):
    leaderboard_data = get_leaderboard(from_time=from_time, to_time=to_time)

    table = Texttable()
    table.set_cols_align(["l", "r", "l"])
    table.add_row(['Rank', 'Name', '🍗'])

    for idx, (user_id, t) in enumerate(leaderboard_data):
        user: User = users.get(user_id)
        user_name = user_id
        if user:
            user_name = user.name
        table.add_row([idx + 1, user_name, f'🍗 x {t}'])
    return f'=== 🍗 {title} 🍗 ===\n```{table.draw()}```'


class ChickensPlugin(MachineBasePlugin):
    def __init__(self, settings, client, storage):
        super().__init__(settings, client, storage)
        self._bot_info = None

    def bot(self) -> dict:
        if not self._bot_info:
            self._bot_info = self.retrieve_bot_info()
        return self._bot_info

    # respond to text with 'phb'
    @respond_to(r'phb')
    def tell_leaderboard(self, msg: Message):
        logging.error(f'tell_leaderboard, {msg}')  # test for a while

        from_time = get_this_monday()
        text = _get_leaderboard_msg_text('本周排行榜', self.users, from_time=from_time)
        msg.say(text)

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
                                          msg_data=msg_data, reaction=AbstractReaction.MENTION_POULTRY_LEG)

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
                                          msg_data=event["item"], reaction=AbstractReaction.REACTION_POULTRY_LEG)
        # self.send_dm(item_user_id, f'<@{user_id}> 热情的给你送了一个的鸡腿')

    @schedule(hour='10', minute='0', day_of_week='mon')
    def leaderboard_weekly(self):
        from_time, to_time = get_prev_monday(), get_this_monday()
        text = _get_leaderboard_msg_text('上周排行榜', self.users, from_time=from_time, to_time=to_time)
        self.say('general', text)
