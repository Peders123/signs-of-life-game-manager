import discord

from discord.ext import commands

from bot.smite import Smite


class SmiteBot(commands.Bot):

    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, command_prefix='!')

    async def add_cogs(self):

        cogs = [Smite(self)]

        for cog in cogs:
            await self.add_cog(cog)

    async def setup_hook(self):

        await self.add_cogs()

    async def on_ready(self):

        print(f'{self.user} has connected to Discord!')

    
