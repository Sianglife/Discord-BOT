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
        
        self.reminder_data = {
            "a" : ["b"]
        }
        # item: [day, second, content]

    # notify on channel
    async def notify(self, item: str):
        channel = self.bot.get_channel(channel_ID)
        embed = discord.Embed(
            title="循環提醒!",
            description=item,
        )
        await channel.send(embed=embed)

    ### schedule
    ## Add item
    async def add_item(self, item: str, day: int, second: int, content: str):
        self.reminder_data[item] = [day, second, content]
        embed = discord.Embed(
            title="已新增提醒", 
            description=f"加入了```{item}```每**{day}天{second}秒**提醒",
            color=discord.Color.green(),
        )
        return embed
    
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
                label="間隔秒數", placeholder="可用符號(如:60*5)，秒為單位",
                default="60",
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
        second = eval(interaction.data["components"][3]["components"][0]["value"])
        embed = await self.add_item(title, day, second, content)
        try:
            self.reminder.add_job(self.notify, "interval", days=day, seconds=second, args=[title], misfire_grace_time=60, id=title)
        except ConflictingIdError:
            embed = discord.Embed(
                title="新增失敗",
                description=f"已經有`{title}`這個提醒了",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        await interaction.response.edit_message(embed=embed, view=None)

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

    ## remove item
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

    # remove item
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

    # List 
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

    # Clear todolist
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