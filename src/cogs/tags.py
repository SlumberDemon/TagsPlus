import discord 
from discord.ext import commands

class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def tag(self, ctx):
        await ctx.send('Placeholder')

def setup(bot):
    bot.add_cog(Tags(bot))
    