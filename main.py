import os

from bot.bot_setup import SmiteBot

from sheets.sheetWrite import *


def run():

    TOKEN = os.getenv('SIGNS_TOKEN')

    bot = SmiteBot()
    bot.setup_hook()
    bot.run(TOKEN)


if __name__ == '__main__':

    run()
