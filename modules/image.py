import discord
from discord.ext import commands
from google_images_search import GoogleImagesSearch

import aiohttp
import os


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="image")
    async def google_image(self, ctx, *, search_param: str = 'cat'):
        """Returns first result of Google Image Search."""
        gis = GoogleImagesSearch(os.getenv("API"), os.getenv("CSE"))

        safe = 'off' if ctx.message.guild is not None and ctx.channel.is_nsfw() else 'high'

        _search_params = {'q': search_param,
                          'num': 1,
                          'searchType': 'image',
                          'safe': safe}

        try:
            gis.search(_search_params)
        except:
            return await ctx.send(
                'Google Error: Please try again or use another search term.\n'
                'If this error persists, it means my daily search limit has been reached and cannot '
                'search anymore due to Google\'s restrictions... \n'
                'Sorry, please try again tomorrow. \U0001f626')

        if gis.results():
            image_url = gis.results()[0].url
        else:
            return await ctx.send(f'Error: Image search for `{search_param}` failed.')

        e = discord.Embed(colour=discord.Colour.green())
        e.set_image(url=image_url)
        e.set_footer(text=f'Google Image Search for: {search_param} — Safe Search: {safe}')

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Images(bot))
    print("Images loaded")
