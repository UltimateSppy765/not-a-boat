import os
import traceback

import discord
from discord.ext import commands, tasks
from imports.modules.gpapi.googleplay import GooglePlayAPI

api = GooglePlayAPI(locale="en_IN", timezone="UTC", device_codename="walleye")
try:
    api.login(gsfId=int(os.environ["GSFID"]), authSubToken=os.environ["AUTHSUBTOKEN"])
except Exception:
    api = None
    err = traceback.format_exc()


class PlayButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="Open in Play Store",
                url="https://play.google.com/store/apps/details?id=com.discord",
                emoji=discord.PartialEmoji(name="play_logo", id=1013122972514537473),
            )
        )


class GPlayScraper(commands.Cog):
    """Discord Android App Version Scanner."""

    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        self.lechannel = self.client.get_channel(1012472180119974069)
        self.lechannel2 = self.client.get_channel(874536637051338772)

    async def cog_load(self) -> None:
        try:
            await self.lechannel.send(
                embed=discord.Embed(
                    description=f"ℹ️ Module `{self.__class__.__name__}` has been initiated.",
                    color=3092791,
                    timestamp=discord.utils.utcnow(),
                )
            )
        except Exception:
            self.ouichannel = False
            async with self.client.httpsession.post(
                "https://discord.com/api/v10/channels/1012472180119974069/messages",
                headers={"Authorization": f"Bot {os.environ['BOAT_TOKEN']}"},
                json={
                    "content": " ".join([f"<@{i}>" for i in self.client.owner_ids]),
                    "embeds": [
                        {
                            "title": "⚠️ There was an error caching the updates channel, unloading extension.",
                            "color": 15548997,
                            "timestamp": discord.utils.utcnow().isoformat(),
                            "description": f"```\n{traceback.format_exc()}\n```",
                        }
                    ],
                },
            ) as response:
                if response.status == 200:
                    return await self.client.unload_extension(
                        "imports.extensions.GPlayScraper"
                    )
                else:
                    self.client.logger.error(
                        "There was a problem while caching the updates channel. Unloading GPlayScraper...",
                        exc_info=1,
                    )
                    return await self.client.unload_extension(
                        "imports.extensions.GPlayScraper"
                    )
        else:
            self.ouichannel = True
        if not api:
            self.client.logger.warning(
                "There was an error while logging in to the Play API."
            )
            embedd = discord.Embed(
                timestamp=discord.utils.utcnow(),
                color=0xED4245,
                title="⚠️ Aborting loop start. There were errors while logging in to the Play API:",
                description=f"```\n{err}\n```",
            )
            embedd.set_footer(
                text="Alpha Update Notifications",
                icon_url="https://static.wikia.nocookie.net/discord/images/4/47/Discord_Canary.png/revision/latest",
            )
            await self.lechannel.send(
                content=" ".join([f"<@{i}>" for i in self.client.owner_ids]),
                embed=embedd,
            )
            return
        self.gplayapi = api
        versiondoc = (
            await self.client.dbclient.collection("stuff").document("version").get()
        )
        self.lastdiscordver = versiondoc.get("lastdiscordver")
        self.redirectview = PlayButton()
        self.discordverscraper.start()

    async def cog_unload(self) -> None:
        if self.ouichannel:
            if api:
                self.discordverscraper.cancel()

    @tasks.loop(minutes=2)
    async def discordverscraper(self) -> None:
        try:
            appdetails = self.gplayapi.details("com.discord")
        except Exception:
            embedd = discord.Embed(
                timestamp=discord.utils.utcnow(),
                color=0xED4245,
                title="⚠️ Stopping loop. There were errors while fetching app details:",
                description=f"```\n{traceback.format_exc()}\n```",
            )
            embedd.set_footer(
                text="Alpha Update Notifications",
                icon_url="https://static.wikia.nocookie.net/discord/images/4/47/Discord_Canary.png/revision/latest",
            )
            await self.lechannel.send(
                content=" ".join([f"<@{i}>" for i in self.client.owner_ids]),
                embed=embedd,
            )
            self.discordverscraper.cancel()
        else:
            embedd = discord.Embed(
                timestamp=discord.utils.utcnow(),
                color=0x5865F2,
                title=appdetails["title"],
                description=(
                    f"**Version:** {appdetails['details']['appDetails']['versionString']} "
                    f"({appdetails['details']['appDetails']['versionCode']})"
                ),
            )
            embedd.set_footer(
                text="Alpha Update Notifications",
                icon_url="https://static.wikia.nocookie.net/discord/images/4/47/Discord_Canary.png/revision/latest",
            )
            embedd.set_image(url=appdetails["image"][0]["imageUrl"])
            embedd.set_thumbnail(url=appdetails["image"][1]["imageUrl"])
            embedd.add_field(
                name="Last Version Code Stored:", value=str(self.lastdiscordver)
            )
            if appdetails["details"]["appDetails"]["versionCode"] != self.lastdiscordver:
                msg = await self.lechannel.send(
                    content="<@&1012474340345917440> Discord version has changed on Play Store!",
                    embed=embedd,
                    view=self.redirectview,
                    allowed_mentions=discord.AllowedMentions(roles=True),
                )
                msg2 = await self.lechannel2.send(
                    content=(
                        "<@&1019276807264018444> Discord version has changed on Play Store!\n"
                        "If you want to get notified for these, toggle the role for yourself using "
                        "</toggle andoot-updates:1020379419082236044>."
                    ),
                    embed=embedd,
                    view=self.redirectview,
                    allowed_mentions=discord.AllowedMentions(roles=True),
                )
                await self.client.dbclient.collection("stuff").document("version").set(
                    {
                        "lastdiscordver": appdetails["details"]["appDetails"][
                            "versionCode"
                        ]
                    }
                )
                await msg.create_thread(
                    name=f"Discord {appdetails['details']['appDetails']['versionString']}",
                    reason=f"Android Discord Update ({appdetails['details']['appDetails']['versionCode']}) Thread",
                )
                await msg2.create_thread(
                    name=f"Discord {appdetails['details']['appDetails']['versionString']}",
                    reason=f"Android Discord Update ({appdetails['details']['appDetails']['versionCode']}) Thread",
                )
                self.lastdiscordver = appdetails["details"]["appDetails"]["versionCode"]


async def setup(client: commands.Bot) -> None:
    await client.add_cog(GPlayScraper(client))
