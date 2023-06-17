from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError

with open("channel_id.json", "r", encoding="utf8") as f:
    channel_ID = int(json.load(f)["schedule"]["id"])


class schedule(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot

        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        self.scheduler.start()

        self.schedule_data = {
            "a" : [datetime.now(), "b"]
        }
        # item: [time, content]

    # notify on channel
    async def notify(self, item: str):
        channel = self.bot.get_channel(channel_ID)
        embed = discord.Embed(
            title="行程提醒!",
            description=f"**{item}**\n{self.schedule_data[item][1]}",
            timestamp=self.schedule_data[item][0],
        )
        self.schedule_data.pop(item)
        await channel.send(embed=embed)

    ### schedule
    ## all command
    @commands.command()
    async def schedule(self, ctx):
        view = discord.ui.View()

        button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="新增行程",
            custom_id="scheadd",
        )
        button.callback = self.scheadd_button_callback
        view.add_item(button)

        button = discord.ui.Button(
            style=discord.ButtonStyle.danger,
            label="刪除行程",
            custom_id="scherm",
        )
        button.callback = self.scherm_button_callback
        view.add_item(button)

        button = discord.ui.Button(
            style=discord.ButtonStyle.secondary,
            label="查看所有行程",
            custom_id="schelist",
        )
        button.callback = self.schelist_button_callback
        view.add_item(button)
        
        await ctx.send(view=view)
        
    ## Add item
    async def add_item(self, item: str, time: datetime, content: str):
        self.schedule_data[item] = [time, content]
        embed = discord.Embed(
            title="已新增行程", 
            description=f"加入了```{item}```於**{time.strftime('%Y/%m/%d %H:%M:%S')}**提醒", 
            color=discord.Color.green(),
        )
        return embed
    
    async def scheadd_button_callback(self, interaction: discord.Interaction):
        self.modal = discord.ui.Modal(title="新增行程")
        self.modal.add_item(
            discord.ui.TextInput(
                label="行程標題", placeholder="請輸入",
                style=discord.TextStyle.long,
                required=True
            ),
        )
        self.modal.add_item(
            discord.ui.TextInput(
                label="行程內容", placeholder="請輸入",
                style=discord.TextStyle.paragraph,
                required=False
            )
        )
        self.modal.add_item(
            discord.ui.TextInput(
                label="日期", placeholder="年/月/日",
                default=f"{str(datetime.now().year)}/{str(datetime.now().month)}/{str(datetime.now().day)}",
                style=discord.TextStyle.short,
                required=True
            )
        )
        self.modal.add_item(
            discord.ui.TextInput(
                label="時間", placeholder="時:分:秒",
                default=f"{str(datetime.now().hour)}:{str(datetime.now().minute+5) if datetime.now().minute<=54 else 5}:{str(datetime.now().second)}",
                style=discord.TextStyle.short,
                required=True
            )
        )
        self.modal.on_submit = self.scheadd_modal_callback
        await interaction.response.send_modal(self.modal)
        
    async def scheadd_modal_callback(self, interaction: discord.Interaction):
        self.modal.stop()
        title = interaction.data["components"][0]["components"][0]["value"]
        content = interaction.data["components"][1]["components"][0]["value"]
        year = int(interaction.data["components"][2]["components"][0]["value"].split("/")[0])
        month = int(interaction.data["components"][2]["components"][0]["value"].split("/")[1])
        day = int(interaction.data["components"][2]["components"][0]["value"].split("/")[2])
        hour = int(interaction.data["components"][3]["components"][0]["value"].split(":")[0])
        minute = int(interaction.data["components"][3]["components"][0]["value"].split(":")[1])
        second = int(interaction.data["components"][3]["components"][0]["value"].split(":")[2])
        time = datetime(year, month, day, hour, minute, second)
        embed = await self.add_item(title, time, content)
        try:
            self.scheduler.add_job(self.notify, "date", run_date=time, args=[title], misfire_grace_time=60, id=title)
        except ConflictingIdError:
            embed = discord.Embed(
                title="新增失敗",
                description=f"已經有`{title}`這個行程了",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        await interaction.response.edit_message(embed=embed, view=None)

    @commands.command()
    async def scheadd(self, ctx):
        # 詢問式輸入
        button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="點擊新增行程",
            custom_id="scheadd",
        )
        button.callback = self.scheadd_button_callback
        view = discord.ui.View()
        view.add_item(button)
        await ctx.send(view=view)

    ## remove item
    async def scherm_button_callback(self, interaction: discord.Interaction):
        if self.schedule_data == {}:
            embed=discord.Embed(
                title="沒有東西可以刪除",
                description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!scheduleadd  -->  新增行程```
                """,
                color=0xff9500
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            select = discord.ui.Select(
                custom_id="schedulerm",
                placeholder="請選擇",
                options=[discord.SelectOption(label=i, value=i) for i in self.schedule_data.keys()]
            )
            select.callback = self.scherm_select_callback
            view = discord.ui.View()
            view.add_item(select)
            await interaction.response.edit_message(embed=embed, view=None)
        await interaction.response.send_message("請選擇要刪除的行程", view=self.modal)

    async def scherm_select_callback(self, interaction: discord.Interaction):
        item = interaction.data["values"][0]
        try:
            self.schedule_data.pop(item)
            self.scheduler.remove_job(item)
        except KeyError:
            embed = discord.Embed(
                title="刪除失敗",
                description=f"沒有`{item}`這個行程",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        
        embed = discord.Embed(
            title="已刪除行程",
            description=f"掰嗶~ `{item}`",
            color=0xff9500
        )
        await interaction.response.edit_message(embed=embed, view=None)

    # remove item
    @commands.command()
    async def scherm(self, ctx):
        if self.schedule_data == {}:
            embed=discord.Embed(
                title="沒有東西可以刪除",
                description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!scheduleadd  -->  新增行程```
                """,
                color=0xff9500
            )
            await ctx.send(embed=embed)
        else:
            # 詢問式輸入
            select = discord.ui.Select(
                custom_id="schedulerm",
                placeholder="請選擇",
                options=[discord.SelectOption(label=i, value=i) for i in self.schedule_data.keys()]
            )
            select.callback = self.scherm_select_callback
            view = discord.ui.View()
            view.add_item(select)
            await ctx.send(view=view)

    # List 
    async def schelist_button_callback(self, interaction: discord.Interaction):
        if len(self.schedule_data) == 0:
            embed=discord.Embed(title="清單沒有東西", description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!scheadd  -->  新增行程```
                """, color=0xff9500)
        else:
            responseText = "\n".join(
                [f"{key} ---> {datetime.strftime(item[0], '%Y/%m/%d %H:%M:%S')}" for key, item in self.schedule_data.items()]
            )
            embed=discord.Embed(
                title="行程列表",
                description=f"```\n{responseText}```",
                color=0x00ff6e
            )
        await interaction.response.edit_message(embed=embed, view=None)

    @commands.command()
    async def schelist(self, ctx):
        if len(self.schedule_data) == 0:
            embed=discord.Embed(title="清單沒有東西", description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!scheadd  -->  新增行程```
                """, color=0xff9500)
        else:
            responseText = "\n".join(
                [f"{key} ---> {datetime.strftime(item[0], '%Y/%m/%d %H:%M:%S')}" for key, item in self.schedule_data.items()]
            )
            embed=discord.Embed(
                title="行程列表",
                description=f"```\n{responseText}```",
                color=0x00ff6e
            )
        await ctx.send(embed=embed)

    

    # Clear todolist
    @commands.command()
    async def scheclear(self, ctx):
        self.schedule_data.clear()
        embed=discord.Embed(title="清空，乾乾淨淨~", description=
            """
            那些事，一去不復返
            """, color=0x00ff6e)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(schedule(bot))