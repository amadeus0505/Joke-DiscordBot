from discord.ext import commands
from resources import bot
import discord
from resources import config
from resources import api_utils


async def raw_joke(ctx, genre):
    joke_line = api_utils.get_random(genre.capitalize())
    await ctx.send(joke_line)


async def raw_prefix(ctx, new):
    if new is None:
        await ctx.send("Current prefix: " + config.get_prefix())
    elif commands.has_permissions(manage_guild=True):
        bot.command_prefix = commands.when_mentioned_or(new)
        config.change_prefix(new)
        await ctx.send("Changed prefix to " + config.get_prefix())
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=f"{config.get_prefix()}help"))
    else:
        await ctx.send("You do not have the permission to use this command!")


async def raw_help(ctx):
    await ctx.message.add_reaction("✅")
    embed = discord.Embed(colour=discord.Colour(0xe18704))
    embed.title = ""
    embed.description = ""
    embed.set_author(name=f"Help for {ctx.author}",
                     icon_url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png")
    embed.set_footer(text=f"Bot made by {bot.get_user(490636491039572009)}")
    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}help", value="show help", inline=False)
    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}joke", value="posts a random joke",
                    inline=False)
    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}joke <genre>",
                    value="posts a joke from a specific genre.\n"
                          "Available genres: dark, miscellaneous, programming", inline=False)

    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}prefix <optional: new prefix>",
                    value="displays or changes the prefix", inline=False)

    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}dj", value="adds the DJ role in order to get "
                    "recognized by Rythm. (Only available if Rythm is on the Server)", inline=False)

    await ctx.author.send(embed=embed)


async def raw_dj(ctx):
    for role in ctx.guild.roles:
        if role.name == "DJ":
            await ctx.author.add_roles(role)
            await ctx.send(f"Glückwunsch {ctx.author.mention}, du bist nun DJ!")
            break
