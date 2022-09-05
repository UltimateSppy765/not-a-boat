import discord


def itr_owner_check(interaction: discord.Interaction) -> bool:
    return interaction.user.id in interaction.client.owner_ids
