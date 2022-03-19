import discord
import aiohttp
from os import getenv
from discord.ext import commands
from dislash import InteractionClient


# Intents
intent = discord.Intents.default()
intent.members = True

# Setup


class Tags(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='+',
            intents=intent,
            case_insensitive=True,
        )
        inter_client = InteractionClient(
            self, 
            modify_send=False
        )
        self.initial_extensions = [
            'cogs.guild',
            'cogs.global',
            'cogs.slash',
        ]

    async def setup_hook(self):
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


tags = Tags()

# Run

tags.run(getenv('TOKEN'))
