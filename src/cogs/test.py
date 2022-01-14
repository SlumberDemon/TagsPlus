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
        try:
            if 0 < len(name) >= 3:
                time = datetime.datetime.now()
                owner = f'{ctx.author.id}'
                await test_guild_create_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": name, "content": content, "created_at": f'{time.day}/{time.month}/{time.year}'}], owner=owner, key=name)
                await ctx.send(f'Tag `{name}` successfully created.')
            else:
                await ctx.send('To `little` characters, please use three or more.')
        except Exception:
            await ctx.send('This tag already exists.')

    @commands.command(name='tags_test')
    async def test_tags(self, ctx, user):
        data = await test_guild_fetch_tag(guild_id=ctx.guild.id, owner=user)
        tags = ''
        for item in data.items:
            tags+=f' {item['key']} \n'
        em = discord.Embed(description=tags)
        await ctx.send(embed=em)


        await ctx.send(data.items)
        await ctx.send(f'This user owns {data.count} Tag(s)')

def setup(bot):
    bot.add_cog(Test(bot))
