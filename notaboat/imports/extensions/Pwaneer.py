from datetime import timedelta

import discord
from discord import app_commands, utils
from discord.ext import commands


@app_commands.guilds(848576409312165908)
class SomeCog(commands.GroupCog, group_name="toggle"):
    def __init__(self) -> None:
        self.updates_role_id = 1019276807264018444

    # Not using check due to a bug on Discord's end.
    # @app_commands.checks.bot_has_permissions(manage_roles=True)
    @app_commands.command(name="andoot-updates")
    @app_commands.checks.cooldown(2, 10)
    async def android_updates_role(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        if interaction.user.get_role(self.updates_role_id):
            await interaction.user.remove_roles(
                discord.Object(self.updates_role_id),
                reason="Toggled Android Updates role.",
            )
            await interaction.followup.send(
                f":white_check_mark: Removed the role <@&{self.updates_role_id}> from you."
            )
        else:
            await interaction.user.add_roles(
                discord.Object(self.updates_role_id),
                reason="Toggled Android Updates role.",
            )
            await interaction.followup.send(
                f":white_check_mark: Added the role <@&{self.updates_role_id}> to you."
            )

    @android_updates_role.error
    async def andoot_role_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            return await interaction.response.send_message(
                content=(
                    ":hourglass: You are on cooldown, you can use the command "
                    f"{utils.format_dt(utils.utcnow() + timedelta(seconds=error.retry_after), 'R')}."
                ),
                ephemeral=True,
            )
        if interaction.response.is_done():
            await interaction.followup.send(
                ":x: There was an error while trying to do what you expected me to do.",
                embed=discord.Embed(
                    description=f"```\n{error}\n```", color=discord.Colour.red()
                ),
            )
        else:
            await interaction.response.send_message(
                ":x: There was an error while trying to do what you expected me to do.",
                embed=discord.Embed(
                    description=f"```\n{error}\n```", color=discord.Colour.red()
                ),
                ephemeral=True,
            )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(SomeCog())
