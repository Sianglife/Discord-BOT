import discord
from discord.ext import commands
import os
from core import Cog_Extension
from random import randint
import time
import asyncio

ans=0

class Game(Cog_Extension):
    # 終極密碼

    def __init__(self, bot):
        super().__init__(bot)
        self.max = 100 
        self.timess=0

    @commands.command()
    async def start(self, ctx):
        #開始玩
        max=self.max 
        min=1
        self.timess=0

        ans=randint(1,101)
        await ctx.send(f'最聰明的{ctx.author.mention}  \n終極密碼要開始羅!')
        

        start_time=time.time()
    

        while True:
            end_time=time.time()
            a=end_time-start_time

            await ctx.send('從%d~%d猜一數字:'%(min,max))
            await ctx.send('請在%d秒內想出來'%(30-a))

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            try:
                msg = await self.bot.wait_for('message',check=check,timeout=(30-a))
                gus = int(msg.content)
                self.timess+=1

            except ValueError:
                await ctx.send('打數字拉 到底喔')
                await asyncio.sleep(2)
                continue

            except asyncio.TimeoutError:
                await ctx.send('時間到! 笑死 想那麼久也太慢 我要去看英文了 呵')
                break


            if gus>=max or gus<=min:
                await ctx.send(f'{ctx.author.mention} 不想玩就別玩 go away')
                await asyncio.sleep(2)
            
            elif gus>ans :
                max=gus

            elif gus<ans:
                min=gus

            else:
                await ctx.send(f'{ctx.author.mention} 唉唷 是電神')
                return False
    
    @commands.command()
    async def set(self,ctx):
        #改範圍
        await ctx.send(f'{ctx.channel.mention} 什麼?想作弊偷改範圍?!')
        await ctx.send("好啦 輸入最大值")
        
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message',check=check,timeout=10)
            self.max = int(msg.content)
            await ctx.send("收到")
        except:
                await ctx.send("你真的很無聊喔")
    
    @commands.command()
    async def grade(self,ctx):
        await ctx.send("你猜了%d次"%(self.timess))
        




async def setup(bot):
    await bot.add_cog(Game(bot))
