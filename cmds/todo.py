from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
import discord

with open("channel_id.json", "r", encoding="utf8") as f:
    channel_ID = int(json.load(f)["todo"]["id"])


class todo(Cog_Extension):
    # Initialization
    def __init__(self, bot):        
        self.todo_data = []

    # 所有功能按鈕一次列出
    @commands.command()
    async def todo(self, ctx):
        view = discord.ui.View()

        button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="新增待辦事項",
            custom_id="todoadd",
        )
        button.callback = self.todoadd_button_callback
        view.add_item(button)

        button = discord.ui.Button(
            style=discord.ButtonStyle.danger,
            label="刪除待辦事項",
            custom_id="todorm",
        )
        button.callback = self.todorm_button_callback
        view.add_item(button)

        button = discord.ui.Button(
            style=discord.ButtonStyle.secondary,
            label="查看所有待辦事項",
            custom_id="todolist",
        )
        button.callback = self.todolist_button_callback
        view.add_item(button)

        await ctx.send(view=view)
        

    # 新增待辦事項專用的函式
    async def add_item(self, item):
        self.todo_data.append(item)
        embed = discord.Embed(
            title="已新增待辦事項", 
            description=f"加入了`{item}`", 
            color=discord.Color.green(),
        )
        return embed
    
    # callbacks for todoadd
    async def todoadd_button_callback(self, interaction: discord.Interaction):
        self.modal = discord.ui.Modal(title="新增代辦事項")
        self.modal.add_item(
            discord.ui.TextInput(
                label="事項名稱", placeholder="請輸入代辦事項",
                style=discord.TextStyle.short
            ),
        )
        self.modal.on_submit = self.todoadd_modal_callback
        await interaction.response.send_modal(self.modal)
        
    async def todoadd_modal_callback(self, interaction: discord.Interaction):
        self.modal.stop()
        item = interaction.data["components"][0]["components"][0]["value"]
        embed = await self.add_item(item)
        await interaction.response.edit_message(embed=embed, view=None)

    # 新增待辦事項的指令
    @commands.command()
    async def todoadd(self, ctx, item: str = ""):
        if item == "":
            # 詢問式輸入
            button = discord.ui.Button(
                style=discord.ButtonStyle.primary,
                label="點擊新增待辦事項",
                custom_id="todoadd",
            )
            button.callback = self.todoadd_button_callback
            view = discord.ui.View()
            view.add_item(button)
            await ctx.send(view=view)
        else:
            # 單次輸入
            embed = self.addItem(item)
            await ctx.send(embed=embed)

    ## callbacks of todorm
    async def todorm_button_callback(self, interaction: discord.Interaction):
        if len(self.todo_data) == 0:
            embed=discord.Embed(
                title="清單沒有東西",
                description="清單空無一物!確認好再問一次吧~",
                color=0xff9500,
            )
            await interaction.response.edit_message(embed=embed, view=None)
            return
        select = discord.ui.Select(
            custom_id="todorm",
            placeholder="請選擇",
            options=[discord.SelectOption(label=i, value=i) for i in self.todo_data]
        )
        select.callback = self.todorm_select_callback
        view = discord.ui.View()
        view.add_item(select)
        await interaction.response.edit_message(view=view)

    async def todorm_select_callback(self, interaction: discord.Interaction):
        item = interaction.data["values"][0]
        self.todo_data.pop(self.todo_data.index(item))
        embed = discord.Embed(title="已刪除待辨事項", description=
            f"掰嗶~ ```{item}```", color=0xff9500)
        await interaction.response.edit_message(embed=embed, view=None)

    # 刪除待辦事項的指令
    @commands.command()
    async def todorm(self, ctx):
        if len(self.todo_data) == 0:
            embed=discord.Embed(
                title="清單沒有東西",
                description="清單空無一物!確認好再問一次吧~",
                color=0xff9500
            )
            await ctx.send(embed=embed)
            return
        select = discord.ui.Select(
            custom_id="todorm",
            placeholder="請選擇",
            options=[discord.SelectOption(label=i, value=i) for i in self.todo_data]
        )
        select.callback = self.todorm_select_callback
        view = discord.ui.View()
        view.add_item(select)
        await ctx.send(view=view)

    # callbacks of todolist
    async def todolist_button_callback(self, interaction: discord.Interaction):
        responseText = "\n".join(self.todo_data)
        if len(self.todo_data) == 0:
            embed=discord.Embed(title="清單沒有東西", description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!todoadd  -->  新增代辦事項```
                """,
                color=0xff9500
            )
        else:
            embed=discord.Embed(title="待辨事項", description=f"```\n{responseText}```", color=0x00ff6e)
        await interaction.response.edit_message(embed=embed, view=None)

    # 列出待辦事項的指令
    @commands.command()
    async def todolist(self, ctx):
        # TODO Embed
        responseText = "\n".join(self.todo_data)
        if len(self.todo_data) == 0:
            embed=discord.Embed(title="清單沒有東西", description=
                """
                清單空無一物!確認好再問一次吧~
                **試試看:**
                ```!todoadd  -->  新增代辦事項```
                """, color=0xff9500)
        else:
            embed=discord.Embed(title="待辨事項", description=f"```\n{responseText}```", color=0x00ff6e)
        await ctx.send(embed=embed)

    # 清空清單
    @commands.command()
    async def todoclear(self, ctx):
        self.todo_data.clear()
        embed=discord.Embed(title="清空，乾乾淨淨~", description=
            """
            那些事項，一去不復返
            """, color=0x00ff6e)
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(todo(bot))