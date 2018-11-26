import os

import delegator
from machine.plugins.base import Message, MachineBasePlugin
from machine.plugins.decorators import respond_to

from gt.libs.docopt import docopt, DocoptExit
from gt.utils.helpers import trim_doc


class YuQuePlugin(MachineBasePlugin):
    """Yuque.

    Usage:
        yuque (-h | --help)
        yuque invite
        yuque add <name>

    Subcommands:
        invite            获取邀请链接
        add <name>        添加到技术组

    Options:
        -h --help     Show this screen.
    """

    prefix = 'yuque'

    @respond_to(rf'\s*{prefix}(?:\s+(?P<arg>.*))?')
    def respond_to_command(self, msg: Message, arg: str):
        arg = arg or ''
        args = list(filter(None, [a.strip() for a in arg.split()]))
        try:
            arguments = docopt(self.__doc__, args)
        except DocoptExit:
            return self.reply_help(msg)
        if arguments.get('-h') or arguments.get('--help'):
            self.reply_help(msg)

        self.process_arguments(msg, arguments)

    def reply_help(self, msg: Message):
        msg.say(trim_doc(self.__doc__), msg.thread_ts)

    def process_arguments(self, msg: Message, arguments: dict):
        subcommand_prefix = 'subcommand_'
        for k in dir(self):
            if not k.startswith(subcommand_prefix):
                continue
            subcommand = k[len(subcommand_prefix):]
            if arguments.get(subcommand):
                f = getattr(self, k)
                if callable(f):
                    f(msg, arguments)

    def subcommand_invite(self, msg: Message, arguments: dict):
        msg.say('正在申请注册链接，请耐心等候...', msg.thread_ts)
        c = delegator.run('python commands/yuque.py invite',
                          cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        if c.ok:
            msg.say(f'注册链接为: {c.out}', msg.thread_ts)
        else:
            msg.say(f'error: {c.err}', msg.thread_ts)

    def subcommand_add(self, msg: Message, arguments: dict):
        name = arguments.get('<name>')
        c = delegator.run(f'python commands/yuque.py add-to-tech-team {name}',
                          cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        if c.ok:
            msg.say(f'已加入语雀技术组', msg.thread_ts)
        else:
            msg.say(f'加入语雀技术组出错', msg.thread_ts)
            msg.say(c.err, msg.thread_ts)
