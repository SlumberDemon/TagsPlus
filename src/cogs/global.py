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

    async def insert_public_tag(self, item: dict, owner_id: int, key: str):
        try:
            self.db.insert(data={'item': item, 'owner': str(owner_id)}, key=key)
            return True
        except Exception:
            return False

    async def fetch_tag_by_owner(self, owner_id: int) -> list:
        return self.db.fetch({"owner": str(owner_id)}).items

    async def get_tag_by_name(self, name: str):
        raw = self.db.get(name)
        if raw:
            return raw
        return None

    async def find_all(self, ctx: commands.Context, query: str):
        results = []
        as_name = await self.get_tag_by_name(query)
        if as_name:
            results.append(as_name)
        if query.isdigit():
            as_id = await self.fetch_tag_by_owner(int(query))
            if as_id:
                results.extend(as_id)
        try:
            user = await commands.UserConverter().convert(ctx, query)
            if user:
                as_user = await self.fetch_tag_by_owner(user.id)
                if as_user:
                    results.extend(as_user)
        except Exception:
            pass

        return [i for n, i in enumerate(results) if i not in results[:n]]

    async def fetch_all_tags(self):
        return self.db.fetch().items


class Global(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.func = AuxFunc()

    @commands.group(name='gtag', invoke_without_command=True)
    async def tag(self, ctx: commands.Context, tag: str):
        pass

    @tag.command(name='add')
    async def gtag_create(self, ctx: commands.Context, name: str, *, content: str):
        if not len(name) < 3:
            time = datetime.datetime.now()
            data = {
                "owner": f'{ctx.author.id}',
                "name": name,
                "content": content,
                "created_at": f'{time.day}/{time.month}/{time.year}'
            }
            check = await self.func.insert_public_tag(item=data, owner_id=ctx.author.id, key=name)
            if check:
                await ctx.send(f'Tag `{name}` created successfully!')
            else:
                await ctx.send(f'Tag {name} already exists.')
        else:
            await ctx.send('Tag name must be at least 3 characters long.')

    @tag.command(name='find')
    async def gtag_find(self, ctx: commands.Context, query: str):
        results = await self.func.find_all(ctx, query)

        def embed_maker(data: dict):
            embed = discord.Embed(title=data['name'], description=data['content'], color=0xffffff)
            embed.set_footer(text=f'Created on {data["created_at"]}')
            return embed

        if results:
            embeds = [embed_maker(data['item']) for data in results]
            await ctx.send(f'**Found {len(results)} Result(s):**', embeds=embeds)
        else:
            await ctx.send('No results found.')


async def setup(bot):
    await bot.add_cog(Global(bot))
