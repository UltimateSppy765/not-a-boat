import time

import discord
from discord.ext import commands
from discord import app_commands, utils
from ..modules.persistentviews import NerdStats


class Miscellaneous(commands.Cog):
    """Miscellaneous commands."""

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction) -> None:
        start = time.perf_counter()
        await interaction.response.defer(ephemeral=True)
        diff = time.perf_counter() - start
        embedd = discord.Embed(
            timestamp=utils.utcnow(),
            colour=7644339,
            description=f":spider_web: REST Latency: `{round(diff*1000)}ms`\n:ping_pong: Websocket Latency: `{round(interaction.client.latency*1000)}ms`",
        )
        embedd.set_author(
            name=interaction.client.user.name,
            icon_url=interaction.client.user.avatar.url,
        )
        await interaction.edit_original_response(embed=embedd, view=NerdStats())


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Miscellaneous(client))
