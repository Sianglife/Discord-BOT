import discord
from discord.ext import commands
import json 
from core import Cog_Extension

class TodoList(Cog_Extension):
    # Initialization 
    def __init__(self, bot):
        self.todo = []
        
    # Add todolist 
    # item 是要增加的待辨事項
    @commands.command()
    async def AddTodoList(self, ctx, item):
        self.todo.append(item)
        await ctx.send(f"已紀錄`{item}`")

    # Remove todolist
    # item 是要移除的待辨事項
    @commands.command()
    async def RemoveTodoList(self, ctx, item):
        self.todo.remove(item)
        await ctx.send(f"已移除`{item}`")

    # Sort todolist
    @commands.command()
    async def SortTodoList(self, ctx):
        # TODO
        # 
        await ctx.send(f"{sorted(self.todo)}")

    # Clear todolist
    @commands.command()
    async def ClearTodoList(self, ctx):
       self.todo.clear()

async def setup(bot):
    await bot.add_cog(TodoList(bot))