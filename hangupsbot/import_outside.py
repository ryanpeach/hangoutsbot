from hangupsbot import get_bot
import hangups
import plugins
import asyncio
import hooks
import sinks
import logging
import time, sys

logger = logging.getLogger()
bot = get_bot()

# def get_custom_on_connect(name):
#     def custom_on_connect(initial_data):
#         plugins.load(bot, name)
#     return custom_on_connect

# def custom_on_connect(initial_data):
#     plugins.load(bot, name)

def custom_connnect(custom_on_connect):
    """Connect to Hangouts and run bot"""
    cookies = bot.login(bot._cookies_path)
    if cookies:
        # Start asyncio event loop
        loop = asyncio.get_event_loop()

        # initialise pluggable framework
        hooks.load(bot)
        sinks.start(bot)

        # Connect to Hangouts
        # If we are forcefully disconnected, try connecting again
        for retry in range(bot._max_retries):
            try:
                # create Hangups client (recreate if its a retry)
                bot._client = hangups.Client(cookies)
                bot._client.on_connect.add_observer(bot._on_connect)
                bot._client.on_connect.add_observer(custom_on_connect)
                bot._client.on_disconnect.add_observer(bot._on_disconnect)

                loop.run_until_complete(bot._client.connect())

                logger.info("bot is exiting")

                loop.run_until_complete(plugins.unload_all(bot))

                bot.memory.flush()
                bot.config.flush()

                sys.exit(0)
            except Exception as e:
                logger.exception("CLIENT: unrecoverable low-level error")
                print('Client unexpectedly disconnected:\n{}'.format(e))

                loop.run_until_complete(plugins.unload_all(bot))

                logger.info('Waiting {} seconds...'.format(5 + retry * 5))
                time.sleep(5 + retry * 5)
                logger.info('Trying to connect again (try {} of {})...'.format(retry + 1, bot._max_retries))

        logger.error('Maximum number of retries reached! Exiting...')

    logger.error("Valid login required, exiting")

    sys.exit(1)
