import discord
from discord.ext import commands


import aiohttp
import os


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="image")
    async def image(self, ctx, search_arg):

        """Searches for a image related to the search arg """
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": os.getenv("API"),
            "cx": os.getenv("CSE"),
            "searchType": "image",
            "q": search_arg,
            "num": 1,
            "safe": "active",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status == 403:
                    return "Limit exceeded"
                data = await resp.json()
                image_url = data[0]["link"]
                # TODO: Check if response is not empty?
                embed = discord.Embed(
                    title=f"{search_arg}".capitalize(), image=image_url
                ).set_image(url=image_url)

                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
    print("Images loaded")
