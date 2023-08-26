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

    @commands.command(description="test for game number")
    async def test_games_num(self, ctx):
        await ctx.reply(self.sheet.get_games_num())

    @commands.command(description="records data from a match")
    async def log_match(self, ctx, match_id, purpose, opponent, password):
        try:
            match_id = int(match_id)
        except ValueError:
            await ctx.reply("Invalid Match Id")

        match = self.api.get_demo_details(match_id)[0]
        players = self.api.get_match_details(match_id)

        team = self.find_team(players)

        date = datetime.strptime(match["Entry_Datetime"], "%m/%d/%Y %H:%M:%S %p")

        data = {
            "match_id": match_id,
            "password": password,
            "date": date.strftime("%d/%m/%Y"),
            "patch": self.api.get_patch_info()['version_string'],
            "purpose": purpose,
            "result": "Victory" if team == match["Winning_Team"] else "Defeat",
            "screenshots": "N/A",
            "vods": "N/A",
            "comments": "N/A"
        }

        data_friendly = {
            "team": ["Signs of Life" for _ in range(5)],
            "player": [x["playerName"] for x in players if x["TaskForce"] == team],
            "kills": [x["Kills_Player"] for x in players if x["TaskForce"] == team],
            "deaths": [x["Deaths"] for x in players if x["TaskForce"] == team],
            "assists": [x["Assists"] for x in players if x["TaskForce"] == team],
            "kda": [round((x["Kills_Player"] + x["Assists"]/2)/max(1, x["Deaths"]), 1) for x in players if x["TaskForce"] == team],
            "kill_participation": [0 for _ in range(5)],
            "gpm": [x["Gold_Per_Minute"] for x in players if x["TaskForce"] == team],
            "damage": [x["Damage_Player"] for x in players if x["TaskForce"] == team],
            "wards": [x["Wards_Placed"] for x in players if x["TaskForce"] == team],
            "damage_structures": [x["Structure_Damage"] for x in players if x["TaskForce"] == team],
            "healing": [x["Healing"] for x in players if x["TaskForce"] == team],
            "god": [x["Reference_Name"] for x in players if x["TaskForce"] == team]
        }

        data_opponent = {

        }

        """for x in players:

            print()
            print(x)
            print()"""

        # self.sheet.write_game_data(data)

    def find_team(self, data):

        players = ["Peders", "Ghaelach", "Cryοnic", "JJMASTER69", "Miltiades"]

        for x in data:

            name = x["playerName"]

            if x["playerName"] and "[" == x["playerName"][0]:

                name = x["playerName"].partition("]")[2]

            if name in players:

                return x["TaskForce"]
