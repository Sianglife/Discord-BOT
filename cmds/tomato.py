from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from threading import Timer
import discord


channel_ID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["time"]["id"])

class tomato(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        self.timer_data = None

    async def notify(self, item: str):
        channel = self.bot.get_channel(channel_ID)
        embed = discord.Embed(
            title="行程提醒!",
            description=f"**{item}**\n{self.schedule_data[item][1]}",
            timestamp=self.schedule_data[item][0],
        )
        self.schedule_data.pop(item)
        await channel.send(embed=embed)

    # start tomato
    @commands.command()
    async def starttomato(self, ctx, n: int=1):
        if self.timer_data != None:
            await ctx.send("已經有一個番茄鐘正在運行中")
            return
        self.timer_data = Timer(5*n, self.notify, args=["番茄鐘"])

    # stop task
    @commands.command()
    async def tasklist(self, ctx):
        outputs = dict()
        for item in self.task:
            outputs[item] = f"{self.task[item][0].strftime('%Y/%m/%d %H:%M:%S')}, 剩餘時間: {(self.task[item][0] - datetime.now()).seconds} 秒"
        await ctx.send(f"目前行程: {dictToStr(outputs, sep2=': ', start='```', end='```')}")
    


async def setup(bot):
    await bot.add_cog(tomato(bot))