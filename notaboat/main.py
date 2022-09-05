import asyncio
import json
import os
from time import perf_counter

import discord
from discord import app_commands
from discord.ext import commands
# from aiohttp import ClientSession
from imports.modules import itrchecks
from imports.modules.persistentviews import perviews
from imports.modules.setuplogger import setuplogger

# Intents stuff
intents = discord.Intents.none()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.messages = True

# Setup logging (Native discord.py logging)
discord.utils.setup_logging(root=False)

with open("notaboat/extensions.json") as file:
    extlist = json.load(file)
# Subclass commands.Bot to allow for stuff like persistent views
class SomeBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            owner_ids={770542184310243342},
            status=discord.Status.do_not_disturb,
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="myself get rebuilt!"
            ),
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False),
        )
        self.initiated = False
        self.logger = setuplogger("BoatBot", 10)
        self.extcache = extlist["extension_list"]
        self.logger.debug(
            "Cached %s extensions from configured list file.", len(self.extcache)
        )

    async def on_ready(self) -> None:
        if not self.initiated:
            self.start_time = discord.utils.utcnow()
            self.logger.debug("No Persistent Views added, adding Persistent Views.")
            for i in perviews():
                self.add_view(i)
            self.persistent_views_added = True
            self.logger.debug(
                "Added %s view%s: %s",
                len(self.persistent_views),
                "" if len(self.persistent_views) == 1 else "s",
                self.persistent_views,
            )
            # Prevent gateway disconnect in case extensions make API calls.
            await asyncio.sleep(2)
            await load_on_start(self)
        self.logger.info("Gateway connection is ready.")
        self.logger.info("Logged in as %s - %s", self.user, self.user.id)


client = SomeBot()


class ExtensionManager(app_commands.Group, name="extension"):
    """Manage the bot's extensions."""

    @app_commands.check(itrchecks.itr_owner_check)
    @app_commands.command()
    async def load(
        self, interaction: discord.Interaction, extension: str | None
    ) -> None:
        if not extension:
            return await interaction.response.send_message("Soon:tm:", ephemeral=True)
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            await client.load_extension(extension)
        except (
            commands.ExtensionAlreadyLoaded,
            commands.ExtensionNotFound,
            commands.ExtensionFailed,
            commands.NoEntryPointError,
        ) as e:
            match e.__class__.__name__:
                case "ExtensionNotFound":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` was not found."
                    )
                case "ExtensionAlreadyLoaded":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` is already loaded."
                    )
                case "NoEntryPointError":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` does not have a `setup` function."
                    )
                case "ExtensionFailed":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` failed to load.",
                        embed=discord.Embed(description=f"```\n{e.original}\n```"),
                    )
        else:
            await interaction.followup.send(
                f":white_check_mark: Successfully loaded the extension `{extension}`."
            )

    @app_commands.check(itrchecks.itr_owner_check)
    @load.autocomplete("extension")
    async def load_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        extlist = client.extcache.keys() - client.extensions
        return [
            app_commands.Choice(name=client.extcache[ext]["nick"], value=ext)
            for ext in extlist
            if current.lower() in ext.lower()
            or current.lower() in client.extcache[ext]["nick"].lower()
        ]

    @app_commands.check(itrchecks.itr_owner_check)
    @app_commands.command()
    async def unload(
        self, interaction: discord.Interaction, extension: str | None
    ) -> None:
        if len(client.extensions) == 0:
            return await interaction.response.send_message(
                ":information_source: There are no extensions to unload.",
                ephemeral=True,
            )
        if not extension:
            return await interaction.response.send_message("Soon:tm:", ephemeral=True)
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            await client.unload_extension(extension)
        except (commands.ExtensionNotFound, commands.ExtensionNotLoaded) as e:
            match e.__class__.__name__:
                case "ExtensionNotFound":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` was not found."
                    )
                case "ExtensionNotLoaded":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` is not loaded."
                    )
        else:
            await interaction.followup.send(
                f":white_check_mark: Successfully unloaded the extension `{extension}`."
            )

    @app_commands.check(itrchecks.itr_owner_check)
    @unload.autocomplete("extension")
    async def unload_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        extlist = client.extensions
        return [
            app_commands.Choice(name=client.extcache[ext]["nick"], value=ext)
            for ext in extlist
            if current.lower() in ext.lower()
            or current.lower() in client.extcache[ext]["nick"].lower()
        ]

    @app_commands.check(itrchecks.itr_owner_check)
    @app_commands.command()
    async def reload(
        self, interaction: discord.Interaction, extension: str | None
    ) -> None:
        if len(client.extensions) == 0:
            return await interaction.response.send_message(
                ":information_source: There are no extensions to reload.",
                ephemeral=True,
            )
        if not extension:
            return await interaction.response.send_message("Soon:tm:", ephemeral=True)
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            await client.reload_extension(extension)
        except (
            commands.ExtensionNotLoaded,
            commands.ExtensionNotFound,
            commands.ExtensionFailed,
            commands.NoEntryPointError,
        ) as e:
            match e.__class__.__name__:
                case "ExtensionNotFound":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` was not found."
                    )
                case "ExtensionNotLoaded":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` is not loaded."
                    )
                case "NoEntryPointError":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` does not have a `setup` function."
                    )
                case "ExtensionFailed":
                    await interaction.followup.send(
                        f":x: Extension `{e.name}` failed to load.",
                        embed=discord.Embed(description=f"```\n{e.original}\n```"),
                    )
        else:
            await interaction.followup.send(
                f":white_check_mark: Successfully reloaded the extension `{extension}`."
            )

    @app_commands.check(itrchecks.itr_owner_check)
    @reload.autocomplete("extension")
    async def reload_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        extlist = client.extensions
        return [
            app_commands.Choice(name=client.extcache[ext]["nick"], value=ext)
            for ext in extlist
            if current.lower() in ext.lower()
            or current.lower() in client.extcache[ext]["nick"].lower()
        ]

    @app_commands.check(itrchecks.itr_owner_check)
    @app_commands.command()
    async def list(
        self, interaction: discord.Interaction, refresh: bool = False
    ) -> None:
        await interaction.response.send_message(str(refresh), ephemeral=True)

    @app_commands.check(itrchecks.itr_owner_check)
    @app_commands.command(name="show-loaded")
    async def showloaded(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Loaded cogs here?", ephemeral=True)

    async def on_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                ":x: You don't have the permission to use this command.", ephemeral=True
            )


client.tree.add_command(ExtensionManager())


async def load_or_fail(client: commands.Bot, extension: str) -> str | None:
    try:
        await client.load_extension(extension)
    except (
        commands.ExtensionNotFound,
        commands.ExtensionFailed,
        commands.NoEntryPointError,
    ) as e:
        match e.__class__.__name__:
            case "ExtensionNotFound":
                client.logger.warning('Extension "%s" was not found.', e.name)
            case "NoEntryPointError":
                client.logger.warning(
                    'Extension "%s" does not have a setup function.', e.name
                )
            case "ExtensionFailed":
                client.logger.error(
                    'Extension "%s" ran into an error while loading:', e.name, exc_info=1
                )
    else:
        return extension


async def load_on_start(client: commands.Bot) -> None:
    client.logger.debug("Loading startup extensions.")
    results = []
    start_time = perf_counter()
    # Loads all extensions and returns a list containing the result values.
    # results = await asyncio.gather(
    #    *(
    #        load_or_fail(client, i)
    #        for i in client.extcache.keys()
    #        if client.extcache[i]["load_on_start"]
    #    )
    # )
    # Leave asyncio.gather here to test for larger number of extensions.
    for i in client.extcache.keys():
        if client.extcache[i]["load_on_start"]:
            results.append(await load_or_fail(client, i))
    end_time = perf_counter()
    # Remove duplicate `None` if any
    results = list(set(results))
    try:
        results.remove(None)
    except ValueError:
        pass
    reslen = len(results)
    client.logger.debug(
        "Successfully loaded %s extension%s in %s second%s.",
        reslen,
        "" if reslen == 1 else "s",
        end_time - start_time,
        "" if end_time - start_time == 1 else "s",
    )
    client.logger.info("Extensions loaded: %s", results)


async def main() -> None:
    async with client:
        await client.start(os.environ["BOAT_TOKEN"])


asyncio.run(main())
