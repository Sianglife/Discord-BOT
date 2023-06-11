from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
from datetime import datetime, timedelta, timezone
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler

Schedule_channelID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["schedule"]["id"])


class Schudule(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        # [time, ]
        self.schedule = dict()
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.scheduler.start()

    # notify on schedule
    async def notify(self, msg):
        channel = self.bot.get_channel(Schedule_channelID)
        await channel.send(f"提醒: {msg}")

    # schedule
    @commands.command()
    async def Sadd(self, ctx, date: str = "", time: str = "", item: str = ""):
        if item == "" or time == "" or date == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            self.schedule[item] = time
            # channel = self.bot.get_channel(Schedule_channelID)
            # channel.send(f"item是{item}, time是{time}")
            l = time.split(":")
            if(len(l) == 2):
                l.append("00")
            lstr = listToStr(l, ":")
            t = datetime.strptime(f"{date} {lstr}",'%Y%m%d %H:%M:%S')
            self.scheduler.add_job(self.notify, "date", run_date=t, args=[item] ,misfire_grace_time=60)
            await ctx.send(f"已新增待辨事項 {item}")

async def setup(bot):
    await bot.add_cog(Schudule(bot))