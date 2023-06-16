from discord.ext import commands
from models.iolib import *
from core import Cog_Extension
import json
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.base import ConflictingIdError
import discord

with open("channel_id.json", "r", encoding="utf8") as f:
    channel_ID = json.load(f)

class Arrangement(Cog_Extension):
    # Initialization
    def __init__(self, bot):
        self.bot = bot
        
        self.todo_data = ['1','2','3']
        self.remind_data = dict() # [string ,days, hour, minute, second]
        self.reminder = AsyncIOScheduler(timezone="Asia/Taipei") 

        self.schedule_data = dict()
        self.scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
        
        self.scheduler.start()
        self.reminder.start()

    # notify on channel
    async def notify(self, msg, d: dict=dict(), item: str = "", channel: str = "", title: str = "提醒"):
        if d != dict() and item != "":
            d.pop(item)
        channel = self.bot.get_channel(channel)
        await channel.send(f"{title}: {msg}")

   
    # schedule
    # add schedule
    @commands.command()
    async def Sadd(self, ctx, date: str = "", time: str = "", item: str = ""):
        if item == "" or time == "" or date == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            self.schedule_data[item] = [time]
            l = time.split(":")
            if(len(l) == 2):
                l.append("00")
            lstr = listToStr(l, ":")
            t = datetime.strptime(f"{date} {lstr}",'%Y%m%d %H:%M:%S')
            try: 
                self.scheduler.add_job(self.notify, "date", run_date=t, args=[item, self.schedule_data, item, channel_ID["schedule"]], misfire_grace_time=60, id=item)
                await ctx.send(f"已新增行程 {item}")
            except ConflictingIdError:
                await ctx.send(f"已有行程 {item}")

    # Remove schedule
    @commands.command()
    async def Srm(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入  
            pass
        else:
            # TODO 單次輸入
            try:
                self.schedule_data.pop(item)
                self.scheduler.remove_job(item)
                await ctx.send(f"已刪除行程 {item}")
            except KeyError:
                await ctx.send(f"沒有這個行程 {item}")

    # List schedule
    @commands.command()
    async def Sout(self, ctx):
        # TODO Embed
        responseText = dictToStr(self.schedule_data, "\n", ": ", "", "", 0)
        await ctx.send(responseText if responseText != "" else "清單沒有東西歐")

    # Clear schedule
    @commands.command()
    async def Sclr(self, ctx):
        self.schedule_data.clear()
        await ctx.send("已清除所有待辨事項")


    # Reminder
    # add reminder
    @commands.command()
    async def Radd(self, ctx, item: str = "", day: int = 0, hour: int = 0, minute: int = 0, second: int = 0):
        if item == "" or (day == 0 and hour == 0 and minute == 0 and second == 0):
            # TODO 詢問式的輸入
            msg = await ctx.send("請輸入提醒事項:")
            message = await ctx.fetch_message(msg.id)
            item = await self.bot.wait_for('message')
            item = item.content
            await message.edit(content=f"新增待辨事項{item}:")
            await ctx.send("請輸入提醒時間:")
        else:            
            # 單次輸入
            pass
        self.reminder.add_job(self.notify, "interval", days=day, hours=hour, minutes=minute, seconds=second, args=[item, self.remind_data, item, channel_ID["reminder"]], misfire_grace_time=60, id=item)
        self.remind_data[item] = [f"{day}天{hour}小時{minute}分鐘{second}秒", day, hour, minute, second]
        embed = discord.Embed(title="已新增待辨事項", description=
            f"加入了`{item}`\n再過`{day}天{hour}小時{minute}分鐘{second}秒`會提醒你", color=0xff9500)
        await ctx.send(embed=embed)

    # Remove reminder
    @commands.command()
    async def Rrm(self, ctx, item: str = ""):
        if item == "":
            # TODO 詢問式的輸入
            pass
        else:
            # TODO 單次輸入
            try:
                self.remind_data.pop(item)
                self.reminder.remove_job(item)
                await ctx.send(f"已刪除行程 {item}")
            except KeyError:
                await ctx.send(f"沒有這個提醒 {item}")

    # List reminder
    @commands.command()
    async def remindlist(self, ctx):
        # TODO Embed
        responseText = dictToStr(self.remind_data, "\n", ": ", "", "", 0)
        await ctx.send(responseText if responseText else "清單沒有東西歐")

    # Clear reminder
    @commands.command()
    async def remindclear(self, ctx):
        self.remind_data.clear()
        embed = discord.Embed(title="已清除所有提醒", description="提醒清單已清空", color=0xff9500)
        await ctx.send(embed=embed)
    
    
    




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
        self.modal.on_submit = self.todo_callback
        await interaction.response.send_modal(self.modal)
        
    async def todo_callback(self, interaction: discord.Interaction):
        self.modal.stop()
        item = interaction.data["components"][0]["components"][0]["value"]
        embed = self.addItem(item)
        await interaction.response.edit_message(embed=embed, view=None)

    @commands.command()
    async def todo(self, ctx, item: str = ""):
        if item == "":
            # 詢問式輸入
            button = discord.ui.Button(
                style=discord.ButtonStyle.green,
                label="點擊選擇刪除的待辦事項",
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
        self.modal = discord.ui.Modal(title="刪除代辦事項")
        self.modal.add_item(
            discord.ui.Select(
                label="刪除事項", placeholder="選擇事項",
                style=discord.TextStyle.long,
                options=[discord.SelectOption(label=item, value=item) for item in self.todo_data]
            ),
        )
        self.modal.on_submit = self.todo_callback
        await interaction.response.send_modal(self.modal)

    async def todorm_callback(self, interaction: discord.Interaction):
        self.modal.stop()
        item = interaction.data["components"][0]["components"][0]["value"]
        print(interaction.data)
        embed = self.addItem(item)
        await interaction.response.edit_message(embed=embed, view=None)

    @commands.command()
    async def todorm(self, ctx, item: str = ""):
        if item == "":
            # 詢問式輸入
            button = discord.ui.Button(
                style=discord.ButtonStyle.green,
                label="點擊新增待辦事項",
                custom_id="todo",
            )
            button.callback = self.remove
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
    await bot.add_cog(Arrangement(bot))