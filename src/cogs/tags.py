import discord 
from discord.ext import commands

class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def tag(self, ctx):
        await ctx.send('Main')

    @tag.command(name='create')
    async def create_tag(self, ctx):
        await ctx.send('Main -> Create')

    @tag.command(name='edit')
    async def edit_tag(self, ctx):
        await ctx.send('Main -> Edit')

    @tag.command(name='delete')
    async def delete_tag(self, ctx):
        await ctx.send('Main -> Delete')

def setup(bot):
    bot.add_cog(Tags(bot))
    