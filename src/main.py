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
            help_command=None
        )

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

# Run

tags = Tags()
tags.run(getenv('TOKEN'))