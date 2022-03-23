import discord
import datetime
from discord.ext import commands
from src.extras.views import Confirm
from src.extras.func import guild_create_tag, guild_fetch_user, guild_edit_tag, guild_delete_tag, guild_get_tag


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test1')
    async def nodata(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data)

    @commands.command(name='test2')
    async def itemdata(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data.items)

    @commands.command(name='test3')
    async def dataname(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data['name'])
        await ctx.send(data['owner'])
        await ctx.send(data['key'])

    @commands.command(name='test5')
    async def datacontent(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data['item'][0]['content'])

    @commands.command(name='test6')
    async def datacreate(self, ctx, name, *, content: str):
        time = datetime.datetime.utcnow()
        owner = f'{ctx.author.id}'
        tag_name = name.replace(' ', '_')
        await guild_create_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": tag_name, "content": content, "created_at": f"{time}"}], owner=owner, name=tag_name)
        await ctx.send(f'Tag `{name}` successfully created.')

    @commands.command(name='test7')
    async def datacreatesingle(self, ctx, name, *, content: str):
        owner = f'{ctx.author.id}'
        tag_name = name.replace(' ', '_')
        await guild_create_tag(guild_id=ctx.guild.id, item=['Item'], owner=owner, name=tag_name)
        await ctx.send(f'Tag `{name}` successfully created.')

async def setup(bot):
    await bot.add_cog(Test(bot))
