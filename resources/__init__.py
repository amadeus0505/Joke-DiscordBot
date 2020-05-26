from discord.ext import commands as dc_commands
import discord
from . import config
import sys


def custom_hook(type, value, tback):
    bot.fetch_user(490636491039572009).send(f"{type} exception caught: {value}")
    sys.__excepthook__(type, value, tback)


sys.excepthook = custom_hook

command_prefix = dc_commands.when_mentioned_or(config.get_prefix())
bot = dc_commands.Bot(command_prefix=command_prefix, help_command=None)
print("version: ", discord.__version__)

from .cogs import commands, events

bot.add_cog(commands.Commands())
bot.add_cog(events.Events())
