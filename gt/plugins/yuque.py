import os

import delegator
from machine.plugins.base import MachineBasePlugin, Message
from machine.plugins.decorators import respond_to


class YuQuePlugin(MachineBasePlugin):
    @respond_to(r'^yuque invitation$')
    def invite(self, msg: Message):
        c = delegator.run('python commands/yuque.py invite', cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        if c.ok:
            msg.say(f'注册链接为: {c.out}', msg.thread_ts)
        else:
            msg.say(c.err, msg.thread_ts)

    @respond_to(r'^yuque add (?P<name>\w+)$')
    def add_to_tech_team(self, msg: Message, name: str):
        c = delegator.run(f'python commands/yuque.py add-to-tech-team {name}', cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        if c.ok:
            msg.say(f'已加入语雀技术组', msg.thread_ts)
        else:
            msg.say(f'加入语雀技术组出错', msg.thread_ts)
            msg.say(c.err, msg.thread_ts)

    @respond_to(r'^yuque help$')
    def invite(self, msg: Message):
        msg.say('''Usage:
        yuque invitation 获取语雀注册邀请链接
        yuque add <name> 加入语雀技术组 
        ''', msg.thread_ts)
