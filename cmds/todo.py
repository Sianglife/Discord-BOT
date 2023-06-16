from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError
import discord

with open("channel_id.json", "r", encoding="utf8") as f:
    channel_ID = json.load(f)["todo"]


class todo(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        
        self.todo_data = ['1','2','3']

    # notify on channel
    async def notify(self, msg, d: dict=dict(), item: str = "", channel: str = "", title: str = "提醒"):
        if d != dict() and item != "":
            d.pop(item)
        channel = self.bot.get_channel(channel)
        await channel.send(f"{title}: {msg}")

   ### todolist
    ## Add item
    async def add_item(self, item):
        self.todo_data.append(item)
        embed = discord.Embed(
            title="已新增待辦事項", 
            description=f"加入了`{item}`", 
            color=discord.Color.green(),
        )
        return embed
    
    async def todo_button_callback(self, interaction: discord.Interaction):
        self.modal = discord.ui.Modal(title="新增代辦事項")
        self.modal.add_item(
            discord.ui.TextInput(
                label="事項名稱", placeholder="請輸入代辦事項",
                style=discord.TextStyle.long
            ),
        )
        self.modal.on_submit = self.todo_modal_callback
        await interaction.response.send_modal(self.modal)
        
    async def todo_modal_callback(self, interaction: discord.Interaction):
        self.modal.stop()
        item = interaction.data["components"][0]["components"][0]["value"]
        embed = await self.add_item(item)
        await interaction.response.edit_message(embed=embed, view=None)

    @commands.command()
    async def todo(self, ctx, item: str = ""):
        if item == "":
            # 詢問式輸入
            button = discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label="點擊新增待辦事項",
                custom_id="todo",
            )
            button.callback = self.todo_button_callback
            view = discord.ui.View()
            view.add_item(button)
            await ctx.send(view=view)
        else:
            # 單次輸入
            embed = self.addItem(item)
            await ctx.send(embed=embed)

    ## remove item
    async def todorm_button_callback(self, interaction: discord.Interaction):
        print(interaction.data)
        # await interaction.response.send_modal(self.modal)

    @commands.command()
    async def todorm(self, ctx, item: str = ""):
        if item == "":
            # 詢問式輸入
            button = discord.ui.Select(
                custom_id="todorm",
                options=[discord.SelectOption(label=i, value=i) for i in self.todo_data]
            )
            button.callback = self.todo_button_callback
            view = discord.ui.View()
            view.add_item(button)
            await ctx.send(view=view)
        else:
            # TODO 單次輸入
            try:
                self.todo_data.pop(self.todo_data.index(item))
                embed = discord.Embed(title="已刪除待辨事項", description=
                    f"掰嗶~ `{item}`", color=0xff9500)
            except ValueError:
                embed=discord.Embed(title="清單沒有這項東西!", description=
                    """
                    從清單找不到你要刪的!加些東西再問一次吧~
                    **試試看:**
                    ```!todolist  -->  列出所有代辦事項```
                    """, color=0xff0000)
            await ctx.send(embed=embed)

    # List todolist
    @commands.command()
    async def todolist(self, ctx):
        # TODO Embed
        responseText = listToStr(self.todo_data, "\n")
        if len(self.todo_data) == 0:
            embed=discord.Embed(title="清單沒有東西", description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!todolist  -->  列出所有待辨事項```
                """, color=0xff9500)
        else:
            embed=discord.Embed(title="待辨事項", description=f"```\n{responseText}```", color=0x00ff6e)
        await ctx.send(embed=embed)

    # Clear todolist
    @commands.command()
    async def todoclear(self, ctx):
        self.todo_data.clear()
        embed=discord.Embed(title="清空，乾乾淨淨~", description=
            """
            那些事項，一去不復返
            """, color=0x00ff6e)
        await ctx.send(embed=embed)

    # search todolist
    @commands.command()
    async def todosearch(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            pass

async def setup(bot):
    await bot.add_cog(todo(bot))