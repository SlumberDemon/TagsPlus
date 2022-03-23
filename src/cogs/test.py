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
    async def datacontent(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data['item'][0]['content'])

async def setup(bot):
    await bot.add_cog(Test(bot))
