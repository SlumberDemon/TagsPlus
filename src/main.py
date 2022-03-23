import os
import discord
from discord.ext import commands


# Intents

intent = discord.Intents.default()
intent.members = True
intent.messages = True
intent.message_content = True

# Prefix

async def custom_prefix(bot, msg):
    return commands.when_mentioned_or('+')(bot, msg)

# Setup

class Tags(commands.Bot):

    __dirs__ = os.listdir('src/cogs')

    def __init__(self):
        super().__init__(intents=intent, command_prefix=custom_prefix)
        self.init_ext = ['cogs.' + file[:-3] for file in self.__dirs__ if file.endswith('.py')]

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        for ext in self.init_ext:
            await self.load_extension(ext)

tags = Tags()

# Run

tags.run(os.getenv('TOKEN'))
