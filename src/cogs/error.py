import discord
from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'Please try again with the `required` argument(s).',
                delete_after=5, 
            )
        else:
            raise error
    
async def setup(bot):
    await bot.add_cog(Error(bot))
