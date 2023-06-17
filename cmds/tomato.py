from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord

channel_ID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["time"]["id"])

class tomato(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        self.timer = AsyncIOScheduler(timezone="Asia/Taipei")
        self.timer.start()
        self.timer_data = None  # datetime

    async def notify(self):
        channel = self.bot.get_channel(channel_ID)
        embed = discord.Embed(
            title="番茄鐘時間到!",
            description=f"休息五分鐘!",
            timestamp=datetime.now()
        )
        self.timer_data = None
        await channel.send(embed=embed)


    # start tomato
    async def starttomato_modal_callback(self, interaction: discord.interactions):
        self.modal.stop()
        n = int(interaction.data["components"][0]["components"][0]["value"])
        # check if n is a number
        if isinstance(n,int) and int(n) > 0:
            self.modal.stop()
            self.timer_data = datetime.now() + timedelta(minutes=int(n))
            self.timer.add_job(self.notify, "date", run_date=self.timer_data)
            await interaction.response.edit_message(content=f"已開始{int(n)}分鐘番茄鐘", view=None)
        else:
            view = discord.ui.View()
            button = discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label="重新輸入",
                custom_id="starttomato_modal_retry",
            )
            button.callback = self.starttomato_select_callback
            view.add_item(button)
            await interaction.response.edit_message(content="請輸入正整數", view=view)

    async def starttomato_select_callback(self, interaction: discord.interactions):
        # print(interaction.data)
        if interaction.data["custom_id"] == "starttomato_modal_retry":
            n = "0"
        else:
            n = interaction.data["values"][0]
        if n == "0":
            self.modal = discord.ui.Modal(
                title="自訂時間"
            )
            self.modal.add_item(
                discord.ui.TextInput(
                    label="時間(分鐘)",
                    placeholder="分鐘"
                )
            )
            self.modal.on_submit = self.starttomato_modal_callback
            await interaction.response.send_modal(self.modal)
        else:
            self.timer_data = datetime.now() + timedelta(minutes=25*int(n))
            self.timer.add_job(self.notify, "date", run_date=self.timer_data)
            await interaction.response.edit_message(content=f"已開始{25*int(n)}分鐘番茄鐘", view=None)

    @commands.command()
    async def starttomato(self, ctx):
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
            custom_id="starttomato_select"
        )
        view.add_item(select)
        select.callback = self.starttomato_select_callback
        await ctx.send("請選擇番茄鐘時間", view=view)
        
    # stop tomato
    @commands.command()
    async def stoptomato(self, ctx):
        if self.timer_data != None:
            self.timer.remove_all_jobs()
            self.timer_data = None
            await ctx.send("已停止番茄鐘")
        else:
            await ctx.send("番茄鐘沒有在運行中")
        

    # view tomato status
    @commands.command()
    async def tomatostatus(self, ctx):
        if self.timer_data != None:
            await ctx.send(f"番茄鐘正在運行中，剩下 {str(self.timer_data - datetime.now()).split('.')[0]}")
        else:
            await ctx.send("番茄鐘沒有在運行中")


async def setup(bot):
    await bot.add_cog(tomato(bot))