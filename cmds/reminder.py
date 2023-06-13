from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from apscheduler.schedulers.asyncio import AsyncIOScheduler

Reminder_channelID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["reminder"]["id"])

class Reminder(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        # [string ,days, hour, minute, second]
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
    async def Radd(self, ctx, item: str = "", day: int = 0, hour: int = 0, minute: int = 0, second: int = 0):
        if item == "" or day == 0 and hour == 0 and minute == 0 and second == 0:
            # TODO 詢問式的輸入
            pass
        else:
            # 單次輸入
            self.remind_data[item] = [f"{day}天{hour}小時{minute}分鐘{second}秒", day, hour, minute, second]
            print(self.remind_data)
            self.reminder.add_job(self.notify, "interval", days=day, hours=hour, minutes=minute, seconds=second, args=[item], misfire_grace_time=60, id=item)
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
                await ctx.send(f"沒有這個提醒 {item}")

    @commands.command()
    async def Rout(self, ctx):
        # TODO Embed
        responseText = dictToStr(self.remind_data, "\n", ": ")
        await ctx.send(responseText if responseText else "清單沒有東西歐")

    # Clear 
    @commands.command()
    async def Rclr(self, ctx):
        self.remind_data.clear()
        await ctx.send("已清除所有待辨事項")

async def setup(bot):
    await bot.add_cog(Reminder(bot))