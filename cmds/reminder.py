from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime, timedelta
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError

with open("channel_id.json", "r", encoding="utf8") as f:
    channel_ID = int(json.load(f)["reminder"]["id"])


class reminder(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot

        self.reminder = AsyncIOScheduler(timezone="Asia/Taipei")
        self.reminder.start()
        
        self.reminder_data = {}
        # 標題: [day: int, hours: int, minutes: int, second: int, 詳細內容: int]

    # 提醒時間到自動呼叫，發送訊息
    async def notify(self, item: str):
        channel = self.bot.get_channel(channel_ID)
        embed = discord.Embed(
            title="循環提醒!",
            description=item,
        )
        await channel.send(embed=embed)

    # 所有功能按鈕一次列出
    @commands.command()
    async def reminder(self, ctx):
        view = discord.ui.View()
        button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="新增提醒",
            custom_id="remiadd",
        )
        button.callback = self.remiadd_button_callback
        view.add_item(button)

        button = discord.ui.Button(
            style=discord.ButtonStyle.danger,
            label="刪除提醒",
            custom_id="remirm",
        )
        button.callback = self.remirm_button_callback
        view.add_item(button)

        button = discord.ui.Button(
            style=discord.ButtonStyle.secondary,
            label="查看所有提醒",
            custom_id="remilist",
        )
        button.callback = self.remilist_button_callback
        view.add_item(button)

        await ctx.send(view=view)

    # 新增提醒專用的函式
    async def add_item(self, item: str, day: int, hours: int, minutes: int, second: int, content: str):
        self.reminder_data[item] = [day, hours, minutes, second, content]
        embed = discord.Embed(
            title="已新增提醒", 
            description=f"加入了```{item}```每**{day}天 {hours}小時 {minutes}分鐘 {second}秒**提醒",
            color=discord.Color.green(),
        )
        return embed
    
    # callbacks of remiadd
    async def remiadd_button_callback(self, interaction: discord.Interaction):
        self.modal = discord.ui.Modal(title="新增提醒")
        self.modal.add_item(
            discord.ui.TextInput(
                label="提醒標題", placeholder="請輸入",
                style=discord.TextStyle.long,
                required=True
            ),
        )
        self.modal.add_item(
            discord.ui.TextInput(
                label="提醒內容", placeholder="請輸入",
                style=discord.TextStyle.paragraph,
                required=False
            )
        )
        self.modal.add_item(
            discord.ui.TextInput(
                label="間隔天數", placeholder="可用符號(如:30*3)，日為單位",
                default="0",
                style=discord.TextStyle.short,
                required=True
            )
        )
        self.modal.add_item(
            discord.ui.TextInput(
                label="間隔時間", placeholder="小時:分鐘:秒鐘",
                default="00:00:59",
                style=discord.TextStyle.short,
                required=True
            )
        )
        self.modal.on_submit = self.remiadd_modal_callback
        await interaction.response.send_modal(self.modal)
        
    async def remiadd_modal_callback(self, interaction: discord.Interaction):
        self.modal.stop()
        title = interaction.data["components"][0]["components"][0]["value"]
        content = interaction.data["components"][1]["components"][0]["value"]
        
        day = eval(interaction.data["components"][2]["components"][0]["value"])
        hours, minutes, second = list(map(int, (interaction.data["components"][3]["components"][0]["value"].split(":"))))
        embed = await self.add_item(title, day, hours, minutes, second, content)
        try:
            self.reminder.add_job(self.notify, "interval", days=day, hours=hours, minutes=minutes, seconds=second, args=[title], misfire_grace_time=60, id=title)
        except ConflictingIdError:
            embed = discord.Embed(
                title="新增失敗",
                description=f"已經有`{title}`這個提醒了",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        await interaction.response.edit_message(embed=embed, view=None)

    # 新增提醒的指令
    @commands.command()
    async def remiadd(self, ctx):
        # 詢問式輸入
        button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="點擊新增提醒",
            custom_id="remiadd",
        )
        button.callback = self.remiadd_button_callback
        view = discord.ui.View()
        view.add_item(button)
        await ctx.send(view=view)

    # callbacks of remirm
    async def remirm_button_callback(self, interaction: discord.Interaction):
        if self.reminder_data == {}:
            embed=discord.Embed(
                title="沒有東西可以刪除",
                description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!remiadd  -->  新增提醒```
                """,
                color=0xff9500
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            # 詢問式輸入
            select = discord.ui.Select(
                custom_id="schedulerm",
                placeholder="請選擇",
                options=[discord.SelectOption(label=i, value=i) for i in self.reminder_data.keys()]
            )
            select.callback = self.remirm_select_callback
            view = discord.ui.View()
            view.add_item(select)
            await interaction.response.edit_message(view=view)

    async def remirm_select_callback(self, interaction: discord.Interaction):
        item = interaction.data["values"][0]
        try:
            self.reminder_data.pop(item)
            self.reminder.remove_job(item)
        except KeyError:
            embed = discord.Embed(
                title="刪除失敗",
                description=f"沒有`{item}`這個提醒",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        embed = discord.Embed(
            title="已刪除提醒",
            description=f"掰嗶~ `{item}`",
            color=0xff9500
        )
        await interaction.response.edit_message(embed=embed, view=None)

    # 刪除提醒的指令
    @commands.command()
    async def remirm(self, ctx):
        if self.reminder_data == {}:
            embed=discord.Embed(
                title="沒有東西可以刪除",
                description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!remiadd  -->  新增提醒```
                """,
                color=0xff9500
            )
            await ctx.send(embed=embed)
        else:
            # 詢問式輸入
            select = discord.ui.Select(
                custom_id="schedulerm",
                placeholder="請選擇",
                options=[discord.SelectOption(label=i, value=i) for i in self.reminder_data.keys()]
            )
            select.callback = self.remirm_select_callback
            view = discord.ui.View()
            view.add_item(select)
            await ctx.send(view=view)

    # callbacks of remilist
    async def remilist_button_callback(self, interaction: discord.Interaction):
        if len(self.reminder_data) == 0:
            embed=discord.Embed(title="清單沒有東西", description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!remiadd  -->  新增提醒```
                """, color=0xff9500)
        else:
            responseText = "\n".join(
                [f"{key} ---> 每{item[0]}天{item[1]}小時{item[2]}分鐘{item[3]}秒提醒" for key, item in self.reminder_data.items()]
            )
            embed=discord.Embed(
                title="提醒列表",
                description=f"```\n{responseText}```",
                color=0x00ff6e
            )
        await interaction.response.edit_message(embed=embed, view=None)

    # 列出提醒的指令
    @commands.command()
    async def remilist(self, ctx):
        if len(self.reminder_data) == 0:
            embed=discord.Embed(title="清單沒有東西", description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!remiadd  -->  新增提醒```
                """, color=0xff9500)
        else:
            responseText = "\n".join(
                [f"{key} ---> {datetime.strftime(item[0], '%Y/%m/%d %H:%M:%S')}" for key, item in self.reminder_data.items()]
            )
            embed=discord.Embed(
                title="提醒列表",
                description=f"```\n{responseText}```",
                color=0x00ff6e
            )
        await ctx.send(embed=embed)

    # 清空提醒的指令
    @commands.command()
    async def remiclear(self, ctx):
        self.reminder_data.clear()
        embed=discord.Embed(title="清空，乾乾淨淨~", description=
            """
            那些事，一去不復返
            """, color=0x00ff6e)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(reminder(bot))