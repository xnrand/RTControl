import supybot.commands


def cmd(*args):
    def cmd_decorator(orig_command):
        def new_command(self, irc, msg, args, *wrapargs):
            try:
                orig_command(self, irc, msg, args, *wrapargs)
            except RTError as e:
                irc.reply(str(e))
        new_command.__doc__=orig_command.__doc__
        return supybot.commands.wrap(new_command, list(args))
    return cmd_decorator

def assertThat(cond, message):
    if not cond:
        raise RTError(message)

class RTError(Exception):
    pass
