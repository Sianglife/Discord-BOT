from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError

Channel_ID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["time_management"]["id"])

class TimeManagement(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        self.task = dict()  # [tdelta]
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.scheduler.start()

    # notify on channel
    async def notify(self, msg, d: dict=dict(), item_id: str = "", channel: str = "", title: str = "提醒"):
        if d != dict() and item_id != "":
            d.pop(item_id)
        channel = self.bot.get_channel(channel)
        await channel.send(f"{title}: {msg}")

    # start task
    @commands.command()
    async def starttask(self, ctx):
        # if start
        pass


    # stop task
    @commands.command()
    async def tasklist(self, ctx):
        outputs = dict()
        for item in self.task:
            outputs[item] = f"{self.task[item][0].strftime('%Y/%m/%d %H:%M:%S')}, 剩餘時間: {(self.task[item][0] - datetime.now()).seconds} 秒"
        await ctx.send(f"目前行程: {dictToStr(outputs, sep2=': ', start='```', end='```')}")
    


async def setup(bot):
    await bot.add_cog(TimeManagement(bot))