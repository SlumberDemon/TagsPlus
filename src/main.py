import os
import discord
from discord.ext import commands
from dislash import InteractionClient


# Intents
intent = discord.Intents.default()
intent.members = True

# Setup


class Tags(commands.Bot):

    __dirs__ = os.listdir('src/cogs')

    def __init__(self):
        super().__init__(intents=intent, command_prefix='+')
        self.init_ext = ['bot.cogs.' + file[:-3] for file in self.__dirs__ if file.endswith('.py')]
        inter_client = InteractionClient(
            self, 
            modify_send=False
        )


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        for ext in self.init_ext:
            await self.load_extension(ext)


tags = Tags()

# Run

tags.run(os.getenv('TOKEN'))