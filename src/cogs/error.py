import discord
from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    ''''

    Single listenener 

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                'Please try again with `required` argument(s).',
                delete_after=10, 
            )

    '''
       
    # Debug listener

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f'```py' f'\n{error}' f'\n```')

def setup(bot):
    bot.add_cog(Error(bot))