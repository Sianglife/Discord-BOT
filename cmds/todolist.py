from discord.ext import commands
from core import Cog_Extension
from models.customReply import GenReply

AddReply = GenReply({
    "OK": ["幫你記錄好{$param}了"],
    "ERR_Nothing": ["你的代辦事項咧？", "你沒有代辦事項喔", "叫你打代辦事項你不打，你要我怎麼幫你記錄", "就叫你打代辦事項了", "沒打代辦事項欺騙我感情，想死嗎！"],
})
RemoveReply = GenReply({
    "OK": ["{$param}，丟了", "{$param}當垃圾了", "{$param}將被我們遺忘"],
    "ERR_Nothing": ["你要丟掉什麼？","你沒給我要刪除的東西喔","你要丟掉什麼要講清楚欸，大膽！說話說一半的！"],
})

class TodoList(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.todo = []

    # Add todolist
    # item 是要增加的待辨事項
    @commands.command()
    async def addtd(self, ctx, item: str = ""):
        if item == "":
            await ctx.send(AddReply.generateReply("ERR_Nothing", msgs=["{$reply}", "```!AddTodoList <待辨事項>```"]))
        else:
            self.todo.append(item)
            await ctx.send(AddReply.generateReply("OK", param=item))

    # Remove todolist
    # item 是要移除的待辨事項
    @commands.command()
    async def rmtd(self, ctx, item: str = ""):
        if item == "":
            await ctx.send(RemoveReply.generateReply("ERR_Nothing", msgs=["{$reply}", "```!RemoveTodoList <待辨事項>```"]))
        else:
            self.todo.remove(item)
            await ctx.send(RemoveReply.generateReply("OK",param=item))

    # Sort todolist
    @commands.command()
    async def sorttd(self, ctx):
        # TODO
        await ctx.send(f"{sorted(self.todo)}")

    # Clear todolist
    @commands.command()
    async def cltd(self, ctx):
        self.todo.clear()


async def setup(bot):
    await bot.add_cog(TodoList(bot))
