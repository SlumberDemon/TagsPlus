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

    @commands.command(name='tag_test')
    async def test_tag_create(self, ctx, name, *, content: str = None):

            if 0 < len(name) >= 3:
                time = datetime.datetime.now()
                owner = f'{ctx.author.id}'
                await test_guild_create_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": name, "content": content, "created_at": f'{time.day}/{time.month}/{time.year}'}], user=owner, key=name)
                await ctx.send(f'Tag `{name}` successfully created.')
            else:
                await ctx.send('To `little` characters, please use three or more.')


def setup(bot):
    bot.add_cog(Test(bot))
