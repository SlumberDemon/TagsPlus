import discord
import datetime
from src.extras.func import *
from src.extras.views import *
from src.extras.emojis import *
from discord.ext import commands


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='emojis')
    async def send_emojis(self, ctx):
        await ctx.send(f'{Emo.Tag} {Emo.Tags} {Emo.TagNotFound} {Emo.TagNeutral} {Emo.TagFound}')

    @commands.command(name='test')
    async def tags(self, ctx, user: discord.User=None):
        user = ctx.author if not user else user
        data = await test_guild_fetch_tag(guild_id=ctx.guild.id, owner=f'{user}')
        tags = ''
        for item in data.items:
            tags+=' ' + item['key'] + ' \n'
        em = discord.Embed(title=f'{user.name}\'s Tags', description=tags)
        em.set_footer(text=f'{data.count} Tag(s)')
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Test(bot))
