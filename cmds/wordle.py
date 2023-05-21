from discord.ext import commands
import json 
from core import Cog_Extension
import requests
import random
from models.customReply import GenReply

startReply = GenReply({
    "OK": ['開始吧！']
})

class Wordle(Cog_Extension):
    # Initialization 
    def __init__(self, bot):
        with open('data.json', 'r', encoding='utf8') as f:
            base_url = json.load(f)['wordleURL']
        r = requests.get(base_url)
        self.words = r.text.split('\n')
        self.bot = bot

    @commands.command()
    async def Play(self, ctx):
        self.answer = random.choice(self.words) # choose a word from list "words"
        await ctx.send(startReply.generateReply("OK", msgs=["{$reply}", "你有五次機會猜出一個單字！使用```!Ask```猜出答案，GoodLuck@@"]))
        
    

    
    @commands.command()
    async def Ask(self, ctx, ans):
        pass 

        '''
        ans 是使用者傳入的猜測答案

        TODO
        1. 沒有play直接ask : 請先輸入 Play 指令
        2. 不是5個字的單字 : 請輸入5個字母的單字
        3. 不是單字的英文組合(不在單字庫中) : 這好像不是個單字
        4. 答對 : 恭喜答對!!!
        5. 猜太多次了 : 真可惜, 答案是{answer}
        '''
        


async def setup(bot):
    await bot.add_cog(Wordle(bot))