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
    async def starttomato_modal_callback(self, interaction: discord.interactions):
        #TODO
        if interaction.data["values"][0] == "0":
            modal = discord.ui.Modal(
                title="自訂時間"
            )
            modal.add_item(
                discord.ui.TextInput(
                    label="時間(分鐘)",
                    placeholder="分鐘"
                )
            )
            modal.callback = self.starttomato_modal_callback

    async def starttomato_select_callback(self, interaction: discord.interactions):
        if interaction.data["values"][0] == "0":
            modal = discord.ui.Modal(
                title="自訂時間"
            )
            modal.add_item(
                discord.ui.TextInput(
                    label="時間(分鐘)",
                    placeholder="分鐘"
                )
            )
            modal.callback = self.starttomato_modal_callback

    @commands.command()
    async def starttomato(self, ctx, n: int=1):
        if self.timer_data != None:
            await ctx.send("已經有一個番茄鐘正在運行中")
            return
        view = discord.ui.View()
        select = discord.ui.Select(
            placeholder="選擇番茄鐘時間",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="25分鐘", value="1"),
                discord.SelectOption(label="50分鐘", value="2"),
                discord.SelectOption(label="100分鐘(1小時40分鐘)", value="3"),
                discord.SelectOption(label="150分鐘(2小時30分鐘)", value="4"),
                discord.SelectOption(label="自訂時間", value="0")
            ],
        )
        view.add_item(select)
        
        self.timer_data = Timer(25*n, self.notify, args=["番茄鐘"])

    # view tomato status
    @commands.command()
    async def tomatostatus(self, ctx):
        if self.timer_data != None:
            await ctx.send("番茄鐘正在運行中")
        else:
            await ctx.send("番茄鐘沒有在運行中")


async def setup(bot):
    await bot.add_cog(tomato(bot))