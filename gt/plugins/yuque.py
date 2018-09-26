import os

import delegator
from machine.plugins.base import MachineBasePlugin, Message
from machine.plugins.decorators import respond_to


class YuQuePlugin(MachineBasePlugin):

    @respond_to(r'yuque\s+invitation')
    def invite(self, msg: Message):
        msg.say('正在申请注册链接，请耐心等候...', msg.thread_ts)
        c = delegator.run('python commands/yuque.py invite', cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        if c.ok:
            msg.say(f'注册链接为: {c.out}', msg.thread_ts)
        else:
            msg.say(f'error: {c.err}', msg.thread_ts)

    @respond_to(r'yuque\s+add\s+(?P<name>\w+)')
    def add_to_tech_team(self, msg: Message, name: str):
        c = delegator.run(f'python commands/yuque.py add-to-tech-team {name}', cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        if c.ok:
            msg.say(f'已加入语雀技术组', msg.thread_ts)
        else:
            msg.say(f'加入语雀技术组出错', msg.thread_ts)
            msg.say(c.err, msg.thread_ts)

    @respond_to(r'yuque\s+help')
    def help(self, msg: Message):
        msg.say('''Usage:
        yuque invitation 获取语雀注册邀请链接
        yuque add <name> 加入语雀技术组 
        ''', msg.thread_ts)
