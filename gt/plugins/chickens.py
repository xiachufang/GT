from typing import Any, Dict

from machine.plugins.base import MachineBasePlugin, Message
from machine.plugins.decorators import respond_to, process
from slackclient.user import User

from ..store.storage import create_user_message_reaction_log, get_leg_leaderboard
from ..utils.helpers import hash_data, json_compact_dumps


class ChickensPlugin(MachineBasePlugin):
    def __init__(self, settings, client, storage):
        super().__init__(settings, client, storage)
        self._bot_info = None

    def bot(self) -> dict:
        if not self._bot_info:
            self._bot_info = self.retrieve_bot_info()
        return self._bot_info

    @respond_to('.*')
    def tell_leaderboard(self, msg: Message):
        leg_leaderboard_data = get_leg_leaderboard()
        lines = ['=== 🍗 排行榜 🍗 ===']
        users = self.users
        for idx, (user_id, t) in enumerate(leg_leaderboard_data):
            user: User = users.get(user_id)
            user_name = user_id
            if user:
                user_name = user.name
            lines.append(f'{idx + 1}. @{user_name} 🍗 x {t}')
        reply = '\n'.join(lines)
        msg.say(reply)

    @process('reaction_added')
    def reaction_to(self, event: Dict[str, Any]):
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
        self.send_dm(item_user_id, f'<@{user_id}> 热情的给你送了一个的鸡腿')
