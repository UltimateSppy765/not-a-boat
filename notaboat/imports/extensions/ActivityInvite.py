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
        activity: discord.Object,
    ) -> None:
        await interaction.response.send_message(
            f"**Channel:** {channel.mention}\n**Activity ID:** {activity.id}",
            ephemeral=True,
        )
        return


async def setup(client: commands.Bot) -> None:
    await client.add_cog(ActivityInvite(client))
