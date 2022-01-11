import discord 
from discord.ext import commands
from src.extras.func import *

class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def tag(self, ctx):
        await ctx.send('Main')

    @tag.command(name='create')
    async def create_tag(self, ctx, name, * content):
        await guild_create_tag(guildId=ctx.guild.id, item=[{"owner":ctx.author.id, "name":name, "content":f"{content}"}], key=name)
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

    @tag.command(name='raw')
    async def raw_tag(self, ctx, tag):
        data = await guild_get_tag(guildId = ctx.guild.id, key=f'{tag}')
        embed = discord.Embed(title=f'Results for [{tag}]', description=f'```py' f'\n{data}' f'\n```')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Tags(bot))
    