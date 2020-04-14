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
            else:
                await message.channel.send("Unable to get command " + stripped[0].strip("!"))


if __name__ == '__main__':
    try:
        with open("token", "r") as token_file:
            token = token_file.read()
    except FileNotFoundError:
        print("You have to create a file named 'token', which contains your bot token")
        exit(0)

    bot = MyClient()
    bot.run(token.strip())


