import discord, datetime 
from discord.ext import commands
from src.extras.func import *

class Tags(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def tag(self, ctx):
        await ctx.send('Main')

    @tag.command(name='create')
    async def create_tag(self, ctx, name, *, content:str):
        try:
            await guild_create_tag(guildId=ctx.guild.id, item=[{"owner":f'{ctx.author.id}', "name":name, "content":content, "created_at":f'{datetime.datetime.utcnow()}'}], key=name)
            await ctx.send(f'Tag {name} successfully created.')
        except:
           await ctx.send('This tag already exists.')

    @tag.command(name='edit')
    async def edit_tag(self, ctx):
        await ctx.send('Main -> Edit')

    @tag.command(name='delete')
    async def delete_tag(self, ctx, tag):
        # await guild_get_tag(guildID=ctx.guild.id, key=tag)
        await ctx.send('Placeholder')

    @tag.command(name='show')
    async def show_tag(self, ctx):
        await ctx.send('Main -> Show')

    @tag.command(name='raw')
    async def raw_tag(self, ctx, tag):
        data = await guild_get_tag(guildId=ctx.guild.id, key=tag)
        embed = discord.Embed(description=f'```py' f'\n{data}' f'\n```')
        await ctx.send(embed=embed)

    @tag.command(name='info')
    async def info(self, ctx, tag):
        # try:
            info = await guild_get_tag(guildId=ctx.guild.id, key=tag)
            embed = discord.Embed(title=info['item'][0]['name'], description='Content ' + info['item'][0]['content'])
            embed.add_field(name='Owner', value='<@' + info['item'][0]['owner'] + '>')
            embed.add_field(name='Created at', value=info['item'][0]['created_at'])

def setup(bot):
    bot.add_cog(Tags(bot))
    