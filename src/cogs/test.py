import discord
import datetime
from discord.ext import commands
from src.extras.views import Confirm
from src.extras.func import guild_create_tag, guild_fetch_user, guild_edit_tag, guild_delete_tag, guild_get_tag


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='1')
    async def test(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data)

    @commands.command(name='2')
    async def test(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data.items)

    @commands.command(name='3')
    async def test(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        await ctx.send(data['item'][0]['content'])

async def setup(bot):
    await bot.add_cog(Test(bot))
