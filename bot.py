import discord
from discord.ext import commands
import config
from api_utils import handle_jokes

command_prefix = commands.when_mentioned_or(config.get_prefix())
bot = commands.Bot(command_prefix=command_prefix)
bot.remove_command("help")

print("version: ", discord.__version__)


@bot.event
async def on_ready():
    print("bot is ready")


@bot.command()
async def joke(ctx, genre="any"):
    joke_line = handle_jokes.get_random(genre.capitalize())
    await ctx.send(joke_line)


@bot.command()
async def prefix(ctx, new=None):
    if new is None:
        await ctx.send("Current prefix: " + config.get_prefix())
    else:
        bot.command_prefix = commands.when_mentioned_or(new)
        config.change_prefix(new)
        await ctx.send("Changed prefix to " + config.get_prefix())


@bot.command(name="help", aliases=["?"])
async def _help(ctx):
    await ctx.message.add_reaction("✅")
    embed = discord.Embed(colour=discord.Colour(0xe18704))
    embed.title = ""
    embed.description = ""
    embed.set_author(name=f"Help for {ctx.author}",
                     icon_url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png")
    embed.set_footer(text=f"Bot made by {bot.get_user(490636491039572009)}")
    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}help", value="show help", inline=False)
    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}joke", value="posts a random joke", inline=False)
    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}joke <genre>",
                    value="posts a joke from a specific genre.\n"
                          "Available genres: dark, miscellaneous, programming", inline=False)

    embed.add_field(name=f"{bot.command_prefix(bot, ctx.message)[-1]}prefix <optional: new prefix>",
                    value="displays or changes the prefix", inline=False)

    await ctx.author.send(embed=embed)


if __name__ == '__main__':
    bot.run(config.get_token())
