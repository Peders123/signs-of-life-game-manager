from discord.ext import commands, tasks

from api.smiteApi import PcSmiteAPI

from sheets.test import main

class Smite(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.api = PcSmiteAPI()

    @commands.command(description="test")
    async def ping(self, ctx):
        await ctx.reply("Pong from {}".format(self.bot.user))

    @commands.command(description="api_test")
    async def test(self, ctx):
        data = self.api.test_session()
        if "Invalid" in data:
            await ctx.reply("Failure")
        else:
            await ctx.reply("Success")

    @commands.command(description="test command for spreadsheet")
    async def test_spreadsheet(self, ctx):
        main()
        await ctx.reply("Success")


    @commands.command(description="records data from a match")
    async def log_match(self, ctx, match_id, purpose, opponent, password):
        try:
            match_id = int(match_id)
        except ValueError:
            await ctx.reply("Invalid Match Id")

        print(data = self.api.get_demo_details(match_id))
