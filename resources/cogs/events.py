from discord.ext.commands import Cog
from resources import bot
import discord
from resources import config


class Events(Cog):

    @Cog.listener()
    async def on_ready(self):
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{config.get_prefix()}help"
            )
        )
        print("bot is ready")

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if (def_role := discord.utils.get(member.guild.roles, name="randoms")) is not None:
            await member.add_roles(def_role)
        else:
            def_role = await member.guild.create_role(name="randoms", color=discord.Colour(0x488579), hoist=True)
            await member.add_roles(def_role)

        if (system_channel := member.guild.system_channel) is not None:
            await system_channel.send(f"Welcome {member.mention} on {member.guild}")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.emoji.name == "📌":
            await bot.http.pin_message(payload.channel_id, payload.message_id)

    @Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        message: discord.Message = reaction.message
        if reaction.emoji == "📌" and reaction.count <= 0:
            await message.unpin()
            await reaction.message.channel.send("Nachricht wurde vom Pinnbrett gelöscht")
