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
    async def start(self, ctx, item: str = "", hours: str = "" , minutes: str = "", seconds: str = ""):
        if item == "" or (hours == "" and minutes == "" and seconds == ""):
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            t = datetime.now() + timedelta(hours=int(hours), seconds=int(seconds))
            self.task[item] = [t]
            try: 
                self.scheduler.add_job(self.notify, "date", run_date=t, args=[item, self.task, item, Channel_ID], misfire_grace_time=60, id=item)
                await ctx.send(f"已新增行程 {item}")
            except ConflictingIdError:
                await ctx.send(f"已有行程 {item}")

    # stop task
    @commands.command()
    async def tasks(self, ctx):
        
        await ctx.send(f"目前行程: {dictToStr(self.task, sep2=': ', start='```', end='```')}")
    


async def setup(bot):
    await bot.add_cog(TimeManagement(bot))