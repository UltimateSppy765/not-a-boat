import disnake as discord
from disnake.ext import commands
from imports.modules.dflow import intent_reply

class Dialog(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.content.startswith('!')==True or message.author.bot==True:
            return
        elif message.guild is not None:
            if self.client.user.mentioned_in(message)==False:
                return
        if message.content.startswith(self.client.user.mention):
            content=message.content.removeprefix(self.client.user.mention)
        else:
            content=message.content
        new_content=await self.replace_mentions(text=content,mentions=message.mentions)
        response=await intent_reply(session_id=f"discord_user_{message.author.id}_{message.channel.id}",text=new_content.strip())
        return await message.reply(response.query_result.fulfillment_text,mention_author=False)

    async def replace_mentions(self,text,mentions):
        for i in mentions:
            text=text.replace(i.mention,i.name)
        return text

    @commands.slash_command()
    async def dialog(self,itr,text:str,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        response=await intent_reply(session_id=f"discord_message_{itr.id}",text=text.strip())
        embed=discord.Embed(color=3092791)
        embed.add_field(name="Text Input",value=f"```\n{text}\n```",inline=False)
        embed.add_field(name="Language",value=f"```\nen-US\n```")
        embed.add_field(name="Intent Detected",value=f"```\n{response.query_result.intent.display_name}\nWith Confidence: {response.query_result.intent_detection_confidence}\n```")
        embed.add_field(name="Fulfillment Text",value=f"```\n{response.query_result.fulfillment_text}\n```",inline=False)
        await itr.edit_original_message(embed=embed)
    
def setup(client):
    client.add_cog(Dialog(client))
