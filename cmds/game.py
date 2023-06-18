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
        #可在命令一起用的變數
        self.max = 100 #最大值
        self.timess=0 #猜的次數

    @commands.command()
    async def start(self, ctx):
        #開始玩
        max=self.max 
        min=1
        self.timess=0

        ans=randint(1,101)

        #終極密碼要開始+遷入訊息
        embed=discord.Embed(title='終極密碼要開始羅!', description=f'最聰明的{ctx.author.mention} 快來發現答案!!', color=0xFF5733)
        await ctx.send(embed=embed)
        

        start_time=time.time()
        #設開始時間
    

        while True:
            
            #設開啟命令的時間
            end_time=time.time()

            #時差(算出開始玩多久了)
            a=end_time-start_time

            #嵌入式訊息!
            embed=discord.Embed(title='遊戲進行中!', description='從%d~%d猜一數字:\n請在%d秒內想出來'%(min,max,(30-a)), color=0xFF5733)
            await ctx.send(embed=embed)

            def check(message):
                #檢查訊息
                return message.author == ctx.author and message.channel == ctx.channel

            try:
                msg = await self.bot.wait_for('message',check=check,timeout=(30-a))
                #等輸入
                gus = int(msg.content)
                #次數加一
                self.timess+=1

            except ValueError:
                #填的東西不是數字
                embed=discord.Embed(title='我生氣了喔', description='打數字拉 到底喔\n 給你休息2秒', color=0xFF5733)
                await ctx.send(embed=embed)
                await asyncio.sleep(2)
                continue

            except asyncio.TimeoutError:
                #時間不夠
                embed=discord.Embed(title='太久了八', description='時間到! 笑死 想那麼久也太慢 我要去看英文了 呵', color=0xFF5733)
                await ctx.send(embed=embed)
                break


            if gus>=max or gus<=min:
                #範圍外
                embed=discord.Embed(title='我生氣了喔', description=f'{ctx.author.mention} 不想玩就別玩 go away', color=0xFF5733)
                await ctx.send(embed=embed)
                await asyncio.sleep(2)
            
            elif gus>ans :
                max=gus

            elif gus<ans:
                min=gus

            else:
                #猜到
                embed=discord.Embed(title='答對!!', description=f'{ctx.author.mention} 唉唷 是電神', color=0xFF5733)
                await ctx.send(embed=embed)

                return False
    
    @commands.command()
    async def set(self,ctx):
        #改範圍
        embed=discord.Embed(title='什麼?想作弊偷改範圍?!', description=f'{ctx.author.mention} 好啦 輸入最大值', color=0xFF5733)
        await ctx.send(embed=embed)

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message',check=check,timeout=10)
            self.max = int(msg.content)

            embed=discord.Embed(title='收到!', color=0xFF5733)
            await ctx.send(embed=embed)

        except:
            embed=discord.Embed(title=f'{ctx.author.mention}你真的很無聊喔',  color=0xFF5733)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def grade(self,ctx):
        #猜的次數9
        embed=discord.Embed(title='你厲害嗎?',description='你猜了%d次'%(self.timess),  color=0xFF5733)
        await ctx.send(embed=embed)

        




async def setup(bot):
    await bot.add_cog(Game(bot))
