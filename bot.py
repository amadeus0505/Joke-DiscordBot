import discord
from discord.ext import commands
import config
from api_utils import handle_jokes

command_prefix = commands.when_mentioned_or(config.get_prefix())
bot = commands.Bot(command_prefix=command_prefix)
bot.remove_command("help")

print("version: ", discord.__version__)

# TODO: add pin function


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{config.get_prefix()}help"
        )
    )
    print("bot is ready")


@bot.event
async def on_member_join(member: discord.Member):
    if (def_role := discord.utils.get(member.guild.roles, name="randoms")) is not None:
        await member.add_roles(def_role)
    else:
        def_role = await member.guild.create_role(name="randoms", color=discord.Colour(0x488579), hoist=True)
        await member.add_roles(def_role)

    if (system_channel := member.guild.system_channel) is not None:
        await system_channel.send(f"Welcome {member.mention} on {member.guild}")


# @bot.event
# async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
#     message: discord.Message = reaction.message
#     if reaction.emoji == "📌":
#         pin_message: discord.Message = await message.pin()


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.emoji.name == "📌":
        await bot.http.pin_message(payload.channel_id, payload.message_id)


@bot.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.Member)
    message: discord.Message = reaction.message
    if reaction.emoji == "📌" and reaction.count <= 0:
        await message.unpin()
        await reaction.message.channel.send("Nachricht wurde vom Pinnbrett gelöscht")


@bot.command()
async def joke(ctx, genre="any"):
    joke_line = handle_jokes.get_random(genre.capitalize())
    await ctx.send(joke_line)


@bot.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, new=None):
    if new is None:
        await ctx.send("Current prefix: " + config.get_prefix())
    else:
        bot.command_prefix = commands.when_mentioned_or(new)
        config.change_prefix(new)
        await ctx.send("Changed prefix to " + config.get_prefix())
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=f"{config.get_prefix()}help"))


@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the permission to use this command!")


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


@bot.command()
async def dj(ctx):
    for role in ctx.guild.roles:
        if role.name == "DJ":
            await ctx.author.add_roles(role)
            await ctx.send(f"Glückwunsch {ctx.author.mention}, du bist nun DJ!")
            break


if __name__ == '__main__':
    bot.run(config.get_token())
