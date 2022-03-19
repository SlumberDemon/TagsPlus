import discord
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
            case_insensitive=True
        )
        inter_client = InteractionClient(
            self, 
            modify_send=False
        )

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


tags = Tags()

# Cogs

cogs = [
    "guild",
    "global",
    "slash"
]

for cog in cogs:
    tags.load_extension("cogs." + cog)

# Run

tags.run(getenv('TOKEN'))