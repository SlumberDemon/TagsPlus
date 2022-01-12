import os
import discord
import datetime
from deta import Deta
from typing import Union
from discord.ext import commands


class AuxFunc:

    def __init__(self):
        self.deta = Deta(os.getenv('DETA'))
        self.db = self.deta.Base('_PUBLIC_TAGS')
        self.cache = self.db.get('all')  # soon implement cache for more efficiency

    async def push_public_tag(self, item: Union[list, dict], key: str):
        return self.db.put({'item': item}, key)

    async def fetch_public_tag(self, key: str):
        data = self.db.get(key)
        if data:
            return data['item']
        else:
            return None


class Global(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.func = AuxFunc()

    @commands.group(name='gtag', invoke_without_command=True)
    async def tag(self, ctx: commands.Context, tag: str):
        data = await self.func.fetch_public_tag(key=tag)
        if data:
            await ctx.send(f'{data}')
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='create')
    async def tag_create(self, ctx: commands.Context, name: str, *, content: str):
        time = datetime.datetime.now()
        keygen = f'{name}_{ctx.author.id}'
        all_tags = await self.func.fetch_public_tag(key='all')
        if all_tags:
            previous = all_tags.get(keygen)
            if previous:
                await ctx.send('Tag already exists.')
            else:
                await ctx.send(f'Tag `{name}` successfully created.')
                all_tags[keygen] = {
                    "owner": f'{ctx.author.id}',
                    "name": name,
                    "content": content,
                    "created_at": f'{time.day}/{time.month}/{time.year}'
                }
                await self.func.push_public_tag(item=all_tags, key=keygen)
        else:
            await ctx.send(f'Tag `{name}` successfully created.')
            item = {
                keygen: {
                    "owner": f'{ctx.author.id}',
                    "name": name,
                    "content": content,
                    "created_at": f'{time.day}/{time.month}/{time.year}'
                }

            }
            await self.func.push_public_tag(item=item, key='all')

    @tag.command(name='raw')
    async def tag_raw(self, ctx: commands.Context, name: str = None, *, user: discord.User = None):
        all_tags = await self.func.fetch_public_tag(key='all')
        if all_tags:
            keys = list(all_tags)
            if name:
                for key in keys:
                    if name in key:
                        await ctx.send(f'```{all_tags[key]}```')

            if user:
                for key in keys:
                    if str(user.id) in key:
                        await ctx.send(f'```{all_tags[key]}```')


def setup(bot: discord.Client):
    bot.add_cog(Global(bot))
