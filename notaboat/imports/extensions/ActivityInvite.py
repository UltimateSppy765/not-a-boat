import discord
from discord import app_commands
from discord.ext import commands

from ..modules import itrchecks


class ActivityInvite(commands.Cog):
    """Commands to create invites to activties in voice channels."""

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.check(itrchecks.itr_owner_check)
    @app_commands.command(name="start-activity")
    async def start_activity(
        self,
        interaction: discord.Interaction,
        channel: discord.VoiceChannel,
        activity: str,
    ) -> None:
        inv = await channel.create_invite(target_application_id=int(activity),target_type=discord.InviteTarget.embedded_application)
        await interaction.response.send_message(
            f"✅ Ok!\n{inv.url}",
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(ActivityInvite(client))
