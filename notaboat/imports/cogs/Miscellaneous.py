import disnake as discord
from disnake.ext import commands
from imports.modules.dflow import intent_reply 

class Whatsup(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=10)

    @discord.ui.button(label="What's Up?",style=discord.ButtonStyle.blurple,emoji="⛵")
    async def watsup(self,btn:discord.ui.Button,itr:discord.Interaction):
        await itr.response.send_message("I'm rowing along the mighty sea shores of the vast oceans of messages you send. It is tiring, isn't it?",ephemeral=True)

    async def on_timeout(self):
        await self.message.edit(view=None)

class Miscellaneous(commands.Cog):
    def __init__(self,client):
        self.client=client
    
    @commands.slash_command()
    async def ping(self,itr):
        await itr.response.send_message(f":sailboat: The time gap between your interaction with me and me rowing up along them is `{round(self.client.latency*1000)}ms`.",ephemeral=True)

    @commands.command()
    async def hello(self,ctx):
        "Just says hello."
        view=Whatsup()
        view.message=await ctx.reply("Hi! I'm Not a Boat!",mention_author=False,view=view)

def setup(client):
    client.add_cog(Miscellaneous(client))
