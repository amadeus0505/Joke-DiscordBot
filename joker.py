from discord import Client
from discord.message import Message
from api_utils import handle_jokes
import discord


class MyClient(Client):
    @staticmethod
    async def on_ready():
        print("Bot is ready")

    async def on_message(self, message: Message):
        if message.author == self.user:
            return
        if message.content.startswith("!"):
            stripped = message.content.split()
            if stripped[0] == "!joke":
                if len(stripped) == 1:
                    joke = handle_jokes.get_random()
                    await message.channel.send(joke)
                elif len(stripped) == 2:
                    joke = handle_jokes.get_random(stripped[1].capitalize())
                    await message.channel.send(joke)
            if stripped[0] == "!help":
                await message.add_reaction("✅")
                embed = discord.Embed(colour=discord.Colour(0xe18704))
                embed.title = ""
                embed.description = ""
                embed.set_author(name=f"Help for {message.author}",
                                 icon_url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png")
                embed.set_footer(text=f"Bot made by {self.get_user(490636491039572009)}")
                embed.add_field(name="!help", value="show help", inline=False)
                embed.add_field(name="!joke", value="posts a random joke", inline=False)
                embed.add_field(name="!joke <genre>",
                                value="posts a joke from a specific genre.\nAvailable genres: dark, "
                                      "miscellaneous, programming", inline=False)
                await message.author.send(embed=embed)
            else:
                await message.channel.send("Unable to get command " + stripped[0].strip("!") + ". Type !help for "
                                                                                               "further information")


if __name__ == '__main__':
    try:
        with open("token", "r") as token_file:
            token = token_file.read()
    except FileNotFoundError:
        print("You have to create a file named 'token', which contains your bot token")
        exit(0)

    bot = MyClient()
    bot.run(token.strip())


