from discord.ext import commands
import discord
from resources import config
from resources import api_utils
from . import raw_commands


class Commands(commands.Cog):
    @commands.command()
    async def joke(self, ctx, genre="any"):
        await raw_commands.raw_joke(ctx, genre)

    @commands.command()
    async def prefix(self, ctx, new=None):
        await raw_commands.raw_prefix(ctx, new)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permission to use this command!")

    @commands.command(name="help", aliases=["?"])
    async def _help(self, ctx):
        await raw_commands.raw_help(ctx)

    @commands.command()
    async def dj(self, ctx):
        await raw_commands.raw_dj(ctx)
