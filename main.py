import os

from bot.bot_setup import client


def run():

    TOKEN = os.getenv('SIGNS_TOKEN')
    client.run(TOKEN)


if __name__ == '__main__':

    run()
