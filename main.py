import os

from bot.bot_setup import SmiteBot

from sheets.test import *


def run():

    TOKEN = os.getenv('SIGNS_TOKEN')

    print(TOKEN)

    bot = SmiteBot()
    bot.setup_hook()
    bot.run(TOKEN)

    """main()"""


if __name__ == '__main__':

    run()
