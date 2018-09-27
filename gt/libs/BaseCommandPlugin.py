import docopt
from machine.plugins.base import MachineBasePlugin, Message
from machine.plugins.decorators import respond_to

from gt.libs.docopt import DocoptExit


class BaseCommandPlugin(MachineBasePlugin):
    """Naval Fate.

    Usage:
      naval_fate.py ship new <name>...
      naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
      naval_fate.py ship shoot <x> <y>
      naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
      naval_fate.py (-h | --help)
      naval_fate.py --version

    Options:
      -h --help     Show this screen.
      --version     Show version.
      --speed=<kn>  Speed in knots [default: 10].
      --moored      Moored (anchored) mine.
      --drifting    Drifting mine.
    """
    prefix = "prefix"

    @respond_to(rf'\s*{prefix}(?:\s+(?P<arg>.*))?')
    def respond_to_command(self, msg: Message, arg: str):
        arg = arg or ''
        args = list(filter(None, [a.strip() for a in arg.split()]))
        try:
            arguments = docopt(self.__doc__, args)
        except DocoptExit as e:
            msg.say(e.usage, msg.thread_ts)
            return
        if arguments.get('-h') or arguments.get('--help'):
            msg.say(self.__doc__, msg.thread_ts)

        self.process_arguments(msg, arguments)

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

    def subcommand_xxx(self, msg: Message, arguments: dict):
        pass
