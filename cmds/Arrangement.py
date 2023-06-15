from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError

channel_ID = dict()
channel_ID["todo"] = int(json.load(open("channel_id.json", "r", encoding="utf8"))["todo"]["id"])
channel_ID["schedule"] = int(json.load(open("channel_id.json", "r", encoding="utf8"))["schedule"]["id"])
channel_ID["reminder"] = int(json.load(open("channel_id.json", "r", encoding="utf8"))["reminder"]["id"])

class Arrangement(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        
        self.todo = list() 
        self.remind_data = dict() # [string ,days, hour, minute, second]
        self.reminder = AsyncIOScheduler(timezone="Asia/Taipei") 

        self.schedule_data = dict()
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        
        self.scheduler.start()
        self.reminder.start()

    # notify on channel
    async def notify(self, msg, d: dict=dict(), item: str = "", channel: str = "", title: str = "提醒"):
        if d != dict() and item != "":
            d.pop(item)
        channel = self.bot.get_channel(channel)
        await channel.send(f"{title}: {msg}")

    
    # schedule
    # add schedule
    @commands.command()
    async def Sadd(self, ctx, date: str = "", time: str = "", item: str = ""):
        if item == "" or time == "" or date == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            self.schedule_data[item] = [time]
            l = time.split(":")
            if(len(l) == 2):
                l.append("00")
            lstr = listToStr(l, ":")
            t = datetime.strptime(f"{date} {lstr}",'%Y%m%d %H:%M:%S')
            try: 
                self.scheduler.add_job(self.notify, "date", run_date=t, args=[item, self.schedule_data, item, channel_ID["schedule"]], misfire_grace_time=60, id=item)
                await ctx.send(f"已新增行程 {item}")
            except ConflictingIdError:
                await ctx.send(f"已有行程 {item}")

    # Remove schedule
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

    # List schedule
    @commands.command()
    async def Sout(self, ctx):
        # TODO Embed
        responseText = dictToStr(self.schedule_data, "\n", ": ", "", "", 0)
        await ctx.send(responseText if responseText != "" else "清單沒有東西歐")

    # Clear schedule
    @commands.command()
    async def Sclr(self, ctx):
        self.schedule_data.clear()
        await ctx.send("已清除所有待辨事項")


    # Reminder
    # add reminder
    @commands.command()
    async def Radd(self, ctx, item: str = "", day: int = 0, hour: int = 0, minute: int = 0, second: int = 0):
        if item == "" or (day == 0 and hour == 0 and minute == 0 and second == 0):
            # TODO 詢問式的輸入
            pass
        else:
            # 單次輸入
            self.remind_data[item] = [f"{day}天{hour}小時{minute}分鐘{second}秒", day, hour, minute, second]
            print(self.remind_data)
            self.reminder.add_job(self.notify, "interval", days=day, hours=hour, minutes=minute, seconds=second, args=[item, self.remind_data, item, channel_ID["reminder"]], misfire_grace_time=60, id=item)
            await ctx.send(f"已新增行程 {item}")

    # Remove reminder
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

    # List reminder
    @commands.command()
    async def Rout(self, ctx):
        # TODO Embed
        responseText = dictToStr(self.remind_data, "\n", ": ", "", "", 0)
        await ctx.send(responseText if responseText else "清單沒有東西歐")

    # Clear reminder
    @commands.command()
    async def Rclr(self, ctx):
        self.remind_data.clear()
        await ctx.send("已清除所有待辨事項")

    # todolist
    # Add todolist
    @commands.command()
    async def Tadd(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            print(item)
            self.todo.append(item)
            await ctx.send(f"已新增待辨事項 {item}")

    # Remove todolist
    @commands.command()
    async def Trm(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            try:
                self.todo.pop(self.todo.index(item))
            except ValueError:
                await ctx.send(f"沒有這個待辨事項 {item}")
            await ctx.send(f"已新增待辨事項 {item}")

    # List todolist
    @commands.command()
    async def Tout(self, ctx):
        # TODO Embed
        responseText = listToStr(self.todo, "\n")
        await ctx.send(responseText if responseText != "" else "清單沒有東西歐")

    # Clear todolist
    @commands.command()
    async def Tclr(self, ctx):
        self.todo.clear()
        await ctx.send("已清除所有待辨事項")

async def setup(bot):
    await bot.add_cog(Arrangement(bot))