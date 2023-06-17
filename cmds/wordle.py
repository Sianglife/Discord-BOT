from discord.ext import commands
from core import Cog_Extension
import random
import requests
from bs4 import BeautifulSoup


class Cmd(Cog_Extension):
    p=0 #遊戲是否進行中
    ch=0 #還有幾次猜的機會
    w=0 #單字庫是否有這個單字
    ans="" #答案
    #爬蟲區
    url ='http://pomeloouo.pythonanywhere.com/' 
    html = requests.get(url)
    html.encoding = 'UTF-8'
    sp = BeautifulSoup(html.text, 'html5lib')
    wo=sp.body.text.split()
    
    @commands.command()
    async def hi(self, ctx):
        await ctx.send("hello")
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')
        
    #玩法教學
    @commands.command()
    async def Wordlehelp(self, ctx):
        await ctx.send(
            """
            > 歡迎來到Wordle遊戲
            > 當你開始一個Wordle遊戲，本機器人將會隨機選取一個長度為5之單字為答案。
            > 接著您可以輸入一個長度為5的單字，注意，必須為一個單字。本機器人會告訴你每個字母有沒有對。
            > 清況分為以下3種:
                > 1.你輸入的單詞該位置字母與答案之字母相同且位置相同，機器人將在該位置輸出**粗體之大寫答案字母**。
                > 2.你輸入的單詞該位置字母與答案之字母相同但位置不同，機器人將在您輸入之位置輸出小寫答案字母。
                > 3.你輸入的單詞該位置字母與答案之字母無相同，機器人將在您輸入之位置輸出⨯。
            > 你可以跟伺服器裡的人一起猜，當然，你們的次數是共用的。
            > 
            > 以下為範例:
                > 答案為apple，您輸入puppy，機器人將輸出:
                > p⨯**P**p⨯⨯
            """
        )
        
    #遊戲啟動
    @commands.command()
    async def Play(self, ctx):
        if self.p==0:
            self.p=1
            self.ch=6
            self.ans=self.wo[random.randrange(14855)] #隨機取
            await ctx.send(f'||{self.ans}||') #我英文太爛需要答案
            await ctx.send(
                """
                ```yaml
                Wordle遊戲開始!
                若需了解規則請輸入$Wordlehelp
                ```
                """
            )
        else:
            await ctx.send(
                """
                ```
                已有遊戲進行中...
                ```
                """
            )
            
    #詢問
    @commands.command()
    async def Ask(self, ctx):
        self.w=0
        ask=''
        ret="""> 
            > """   #猜字提示
        over="""```yaml
            遊戲結束!
            答案是"""#未猜中文字
        win="""```yaml
            恭喜猜對~
            答案是"""#猜中文字
        if self.p==1:
            if len(ctx.message.content)==10: #檢測是否為五個字母
                msg=ctx.message.content[5:].lower() #取出單字部分(去掉$Ask )
                for i in self.wo:
                    if msg==i:
                        self.w=1
                        ask=msg #確認為單字後檢測各字母用
                if self.w ==1:
                    self.ch-=1
                    for i in range(5):#檢測字母
                        if ask==self.ans:#答對時
                            self.p=0
                            win+=self.ans#答案
                            win+="""
                                你花了
                            """
                            win+=str(6-self.ch)#次數
                            win+="次猜中```"
                            await ctx.send(win)
                            break
                        if ask[i]==self.ans[i]:
                            ret+="**"
                            ret+=self.ans[i].upper()
                            ret+="** "
                        elif ask[i] in self.ans:
                            ret+=ask[i]
                            ret+=" "
                        else:
                            ret+='⨯ '
                    if self.p==1:#以免猜中後又輸出
                        await ctx.send(ret)
                    if self.ch==0 and self.p==1:#次數耗盡未猜出
                        self.p=0
                        over+=self.ans
                        over+="```"
                        await ctx.send(over)
                else:
                    await ctx.send(
                        """
                        ```
                        這不是個單字喲!
                        ```
                        """
                    )#非單字
            else:
                await ctx.send(
                    """
                    ```
                    請輸入長度為5的單詞~
                    ```
                    """
                )#長度不為5
        else:
            await ctx.send(
                """
                ```
                請先使用$Play指令開始遊戲:)
                ```
                """
            )#未開啟遊戲

async def setup(bot):
    await bot.add_cog(Cmd(bot))