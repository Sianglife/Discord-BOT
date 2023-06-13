from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
from datetime import datetime
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError

Schedule_channelID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["schedule"]["id"])


class Schudule(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        # [time, ]
        self.schedule_data = dict()
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.scheduler.start()

    # notify on schedule
    async def notify(self, msg, d: dict=dict(), item: str = ""):
        if d != dict() and item != "":
            d.pop(item)
        channel = self.bot.get_channel(Schedule_channelID)
        await channel.send(f"行程: {msg}")

    # schedule
    @commands.command()
    async def Sadd(self, ctx, date: str = "", time: str = "", item: str = ""):
        if item == "" or time == "" or date == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            self.schedule_data[item] = time
            l = time.split(":")
            if(len(l) == 2):
                l.append("00")
            lstr = listToStr(l, ":")
            t = datetime.strptime(f"{date} {lstr}",'%Y%m%d %H:%M:%S')
            try: 
                self.scheduler.add_job(self.notify, "date", run_date=t, args=[item, self.schedule_data, item], misfire_grace_time=60, id=item)
                await ctx.send(f"已新增行程 {item}")
            except ConflictingIdError:
                await ctx.send(f"已有行程 {item}")

    # Remove todolist
    @commands.command()
    async def Srm(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入  
            pass
        else:
            # TODO 單次輸入
            try:
                self.schedule_data.pop(item)
                self.scheduler.remove_job(item)
                await ctx.send(f"已刪除行程 {item}")
            except KeyError:
                await ctx.send(f"沒有這個行程 {item}")

    @commands.command()
    async def Sout(self, ctx):
        # TODO Embed
        responseText = dictToStr(self.schedule_data, "\n", ": ")
        await ctx.send(responseText if responseText != "" else "清單沒有東西歐")

    # Clear 
    @commands.command()
    async def Sclr(self, ctx):
        self.schedule_data.clear()
        await ctx.send("已清除所有待辨事項")

async def setup(bot):
    await bot.add_cog(Schudule(bot))