from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
from datetime import datetime
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler

Reminder_channelID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["reminder"]["id"])

class Reminder(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        # [months, hour, minute, second, intervel(seconds)]
        self.remind_data = dict()
        self.reminder = AsyncIOScheduler(timezone="Asia/Taipei")
        self.reminder.start()

    # notify on schedule
    async def notify(self, msg, d: dict=dict(), item: str = ""):
        if d != dict() and item != "":
            d.pop(item)
        channel = self.bot.get_channel(Reminder_channelID)
        await channel.send(f"提醒: {msg}")

    # schedule
    @commands.command()
    async def Radd(self, ctx, ymd: str = "", hms = "", item: str = ""):
        if item == "" or ymd == "" and hms == "":
            # TODO 詢問式的輸入
            pass
        else:
            # 單次輸入
            d = datetime.strptime(f"{ymd} {hms}", "%Y/%m/%d %H:%M:%S")
            self.remind_data[item] = d
            self.reminder.add_job(self.notify, "interval", run_date=d, args=[item, self.schedule, item], misfire_grace_time=60, id=item)
            await ctx.send(f"已新增行程 {item}")

    # Remove todolist
    @commands.command()
    async def Rrm(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            try:
                self.remind_data.pop(item)
                self.reminder.remove_job(item)
                await ctx.send(f"已刪除行程 {item}")
            except KeyError:
                await ctx.send(f"沒有這個行程 {item}")

    @commands.command()
    async def Rout(self, ctx):
        # TODO Embed
        responseText = dictToStr(self.remind_data, "\n", ": ")
        await ctx.send(responseText if responseText != "" else "清單沒有東西歐")

    # Clear 
    @commands.command()
    async def Rclr(self, ctx):
        self.remind_data.clear()
        await ctx.send("已清除所有待辨事項")

async def setup(bot):
    await bot.add_cog(Reminder(bot))