import discord
import datetime

from discord import guild
from src.extras.func import *
from src.extras.func import test_guild_get_user_tags
from src.extras.views import *
from src.extras.emojis import *
from discord.ext import commands


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='emojis')
    async def send_emojis(self, ctx):
        await ctx.send(f'{Emo.Tag} {Emo.Tags} {Emo.TagNotFound} {Emo.TagNeutral} {Emo.TagFound}')

    @commands.command(name='tag_test') # idk the command storing works but still gives error. checked the db and the item got created
    async def test_tag_create(self, ctx, name, *, content: str = None):
        try:
            if 0 < len(name) >= 3:
                time = datetime.datetime.now()
                owner = f'{ctx.author.id}'
                await test_guild_create_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": name, "content": content, "created_at": f'{time.day}/{time.month}/{time.year}'}], user=owner, key=name)
                await ctx.send(f'Tag `{name}` successfully created.')
            else:
                await ctx.send('To `little` characters, please use three or more.')
        except Exception:
            await ctx.send('This tag already exists.')

    @commands.command(name='tags_test')
    async def test_tags(self, ctx, tag):
        data = await test_guild_get_user_tags(guild_id=ctx.guild.id, user=f'{ctx.author.id}')
        await ctx.send(data)

def setup(bot):
    bot.add_cog(Test(bot))
