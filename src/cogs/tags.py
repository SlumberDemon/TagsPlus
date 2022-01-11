import discord 
from discord.ext import commands
from src.extras.func import *
from src.extras.func import guild_create_tag

class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def tag(self, ctx):
        await ctx.send('Main')

    @tag.command(name='create')
    async def create_tag(self, ctx, name, * content):
        await guild_create_tag(guildId=ctx.guild.id, item=[{"owner":ctx.author.id, "name":name, "content":content}], key=name)
        await ctx.send(f'Created tag "{name}"')

    @tag.command(name='edit')
    async def edit_tag(self, ctx):
        await ctx.send('Main -> Edit')

    @tag.command(name='delete')
    async def delete_tag(self, ctx):
        await ctx.send('Main -> Delete')

    @tag.command(name='show')
    async def show_tag(self, ctx):
        await ctx.send('Main -> Show')

def setup(bot):
    bot.add_cog(Tags(bot))
    