from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json

Schedule_channelID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["schedule"]["id"])

class Schudule(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.todo = []

    # todo
    @commands.command()
    async def Sadd(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            print(item)
            self.todo.append(item)
            await ctx.send(f"已新增待辨事項 {item}")

async def setup(bot):
    await bot.add_cog(Schudule(bot))