import hangups
from hangupsbot.hangupsbot import get_bot
from hangupsbot.handlers import handler
from hangupsbot.commands import command

bot = get_bot()
handler.set_bot(bot)
@handler.register(priority=5, event=hangups.ChatMessageEvent)
def receive_message(bot, event, *args):
    print("hello world!")

print(handler)
bot.run()
