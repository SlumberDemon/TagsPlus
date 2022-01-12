import discord
from discord.ext import commands
from os import getenv

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

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


tags = Tags()

# Cogs

cogs = [
    "guild",
    "global",
    "error"
]

for cog in cogs:
    tags.load_extension("cogs." + cog)

# Run

tags.run(getenv('TOKEN'))
