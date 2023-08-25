from datetime import datetime

from discord.ext import commands, tasks

from api.smiteApi import PcSmiteAPI

from sheets.sheetWrite import Sheet

class Smite(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.api = PcSmiteAPI()
        self.sheet = Sheet()

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

    @commands.command(description="records data from a match")
    async def log_match(self, ctx, match_id, purpose, opponent, password):
        try:
            match_id = int(match_id)
        except ValueError:
            await ctx.reply("Invalid Match Id")

        match = self.api.get_demo_details(match_id)[0]

        date = datetime.strptime(match["Entry_Datetime"], "%m/%d/%Y %H:%M:%S %p")

        # print(self.api.get_patch_info()['version_string'])

        data = {
            "match_id": match_id,
            "password": password,
            "date": date.strftime("%d/%m/%Y"),
            "patch": self.api.get_patch_info()['version_string'],
            "purpose": purpose,
            "result": match["Winning_Team"],
            "screenshots": "N/A",
            "vods": "N/A",
            "comments": "N/A"
        }

        self.sheet.write_game_data(data)
