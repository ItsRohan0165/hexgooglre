import discord
from discord.ext import commands

import aiohttp
import os


class Fornite:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="fortnite")
    async def fortnite(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "Invalid fortnite command, please type !help fortnite for usage"
            )

    @fortnite.command(name="store")
    async def get_shop_items(self, ctx):
        """Retrieves the items that are currently in the fortnite store"""

        url = "https://api.fortnitetracker.com/v1/store"
        header = {"TRN-Api-Key": os.getenv("FORTNITE_API_TN_KEY")}

        async with aiohttp.ClientSession(headers=header) as session:
            async with session.get(url) as resp:
                data = await resp.json()
                embed = discord.Embed(
                    title="Store",
                    url="https://fortnitetracker.com/shop",
                    description="Available items in the fortnite store",
                    color=0xD42B2D,
                )
                embed.set_thumbnail(
                    url="http://pixelartmaker.com/art/66a497e3c4a8b3a.png"
                )
                embed.set_footer(
                    text="For more info visit https://fortnitetracker.com/shop"
                )
                for value in data:
                    embed.add_field(
                        name=value["name"],
                        value=f"vBucks: {value['vBucks']}",
                        inline=True,
                    )

                await ctx.send(embed=embed)

    @fortnite.command(name="stats")
    async def get_match_history(self, ctx):

        """Retrieves the match history of a specific player in a platform"""


def setup(bot):
    bot.add_cog(Fornite(bot))
