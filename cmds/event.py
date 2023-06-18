from dotenv import load_dotenv
from discord.ext import commands
import json
from core import Cog_Extension

load_dotenv()
channel_id = int(json.load(open("channel_id.json", "r", encoding="utf8"))["welcome"]["id"])

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        g_channel = self.bot.get_channel(int(json.load(open("channel_id.json", "r", encoding="utf8"))["welcome"]["id"]))
        await g_channel.send(f"歡迎{member}加入!")

    '''
    TODO (optional)
    Add other events such as on_message, on_command_error
    '''
    
async def setup(bot):
    await bot.add_cog(Event(bot))