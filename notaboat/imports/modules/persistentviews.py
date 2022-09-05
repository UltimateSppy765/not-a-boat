import platform
from sys import version
from time import perf_counter

import discord


def perviews() -> list[discord.ui.View]:
    return [NerdStats(), NoNerdStats()]


class NerdStats(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Stats for Nerds",
        custom_id="nerdstats",
        emoji="ℹ️",
        style=discord.ButtonStyle.blurple,
    )
    async def nerdstatsbtn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        embedd = discord.Embed(
            timestamp=discord.utils.utcnow(),
            colour=7644339,
            description=f":nut_and_bolt: **Codebase:** Python\n<:python:596577462335307777> **Language Version:** Python {version}\n<:dpy:596577034537402378> **Discord API Library:** discord.py [v{discord.__version__}](https://github.com/Rapptz/discord.py/tree/v{discord.__version__})\n:clock10: **Running since:** {discord.utils.format_dt(interaction.client.start_time, 'R')}\n:gear: **Operating System:** {platform.platform(terse=True)}",
        )
        embedd.set_author(
            name=interaction.client.user.name,
            icon_url=interaction.client.user.avatar.url,
        )
        await interaction.response.edit_message(embed=embedd, view=NoNerdStats())


class NoNerdStats(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(
        label="This is too nerdy for me.",
        custom_id="nonerdstats",
        emoji="💭",
        style=discord.ButtonStyle.blurple,
    )
    async def nonerdstatsbtn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        start = perf_counter()
        await interaction.response.defer()
        diff = perf_counter() - start
        embedd = discord.Embed(
            timestamp=discord.utils.utcnow(),
            colour=7644339,
            description=f":spider_web: REST Latency: `{round(diff*1000)}ms`\n:ping_pong: Websocket Latency: `{round(interaction.client.latency*1000)}ms`",
        )
        embedd.set_author(
            name=interaction.client.user.name,
            icon_url=interaction.client.user.avatar.url,
        )
        await interaction.edit_original_response(embed=embedd, view=NerdStats())
