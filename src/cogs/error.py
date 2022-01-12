import discord
from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        user = ctx.author
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'Please try again with `required` argument(s).',
                delete_after=10, 
            )

def setup(bot):
    bot.add_cog(Error(bot))