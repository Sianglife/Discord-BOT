from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json

TODO_channelID = int(json.load(open("channel_id.json", "r", encoding="utf8"))["todo"]["id"])

class TodoList(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.todo = list()

    # todo
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
            print(item)
            self.todo.append(item)
            await ctx.send(f"已新增待辨事項 {item}")

    # Sort todolist
    @commands.command()
    async def Tout(self, ctx):
        # TODO Embed
        print(self.todo)
        responseText = listToStr(self.todo, "\n")
        await ctx.send(responseText if responseText != "" else "清單沒有東西歐")

    # Clear todolist
    @commands.command()
    async def Tclr(self, ctx):
        self.todo.clear()
        # TODO
        await ctx.send("已清除所有待辨事項")


async def setup(bot):
    await bot.add_cog(TodoList(bot))
