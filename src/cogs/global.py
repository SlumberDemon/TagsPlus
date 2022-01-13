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
        self.cache = self.db.get('all')

    async def push_public_tag(self, item: dict, key: str):
        await self.update_cache(item)
        return self.db.put({'item': item}, key)

    async def fetch_public_tag(self, key: str):
        data = self.db.get(key)
        if data:
            return data.get('item')
        return None

    async def get_cached_tags(self):
        if self.cache:
            return self.cache.get('item')
        return None

    async def update_cache(self, item: dict):
        self.cache = {'item': item}


class Global(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.func = AuxFunc()

    @commands.group(name='gtag', invoke_without_command=True)
    async def tag(self, ctx: commands.Context, tag: str):
        all_tags = await self.func.get_cached_tags()
        if all_tags:
            keys = list(all_tags)
            for key in keys:
                if tag in key:
                    tag_id = key.replace(f'_', ' ').split(' ')[1]
                    emd = discord.Embed(
                        title=f'{all_tags[key]["name"]}',
                        description=f'{all_tags[key]["content"]}',
                        color=0x36393f
                    )
                    emd.set_footer(text=f'Created by {self.bot.get_user(int(tag_id))} | (id: {tag_id})')
                    await ctx.send(embed=emd)
                    return
            else:
                await ctx.send('Tag not found.')

    @tag.command(name='create')
    async def tag_create(self, ctx: commands.Context, name: str, *, content: str):
        if not len(name) < 3:
            time = datetime.datetime.now()
            keygen = f'{name}_{ctx.author.id}'
            all_tags = await self.func.get_cached_tags()
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
                    await self.func.push_public_tag(item=all_tags, key='all')
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
        else:
            await ctx.send('Tag name must be at least 3 characters long.')

    @tag.command(name='raw')
    async def tag_raw(
            self,
            ctx: commands.Context,
            name: str = None,
            owner: Union[discord.User, discord.Member] = None
    ):
        all_tags = await self.func.get_cached_tags()
        if all_tags:
            keys = list(all_tags)
            if name:
                for key in keys:
                    if name in key:
                        await ctx.send(f'```{all_tags[key]}```')

            if owner:
                for key in keys:
                    if str(owner.id) in key:
                        await ctx.send(f'```{all_tags[key]}```')

    @tag.command(name='all')
    async def tag_raw(self, ctx: commands.Context):
        all_tags = await self.func.get_cached_tags()
        string = ''
        if all_tags:
            keys = list(all_tags)
            _replaced = [item.replace('_', ' ') for item in keys]
            tup_data = [item.split(' ') for item in _replaced]
            for item in tup_data:
                string += f'**{item[0]}** (id: {item[1]})\n\n'
            await ctx.send(embed=discord.Embed(title='All Global Tags', description=f'{string}', color=0x36393f))


def setup(bot: discord.Client):
    bot.add_cog(Global(bot))
