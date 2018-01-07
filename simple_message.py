import hangups
from hangupsbot.hangupsbot import get_bot
from hangupsbot.handlers import handler
from hangupsbot.commands import command
from hangupsbot.plugins import tracking, load_functions

bot = get_bot()

@handler.register(priority=5, event=hangups.ChatMessageEvent)
def receive_message(bot, event, *args):
    print("hello world!")


@command.register(admin=False, plugin=False)
def helloworld(bot, event, *args):
    print("hello world!2")

load_functions(bot, "__main__", "", [("helloworld", helloworld)])
bot.run()
