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

    async def push_public_tag(self, item: dict, owner_id: int, key: str):
        return self.db.put({'item': item, 'owner': str(owner_id)}, key)

    async def insert_public_tag(self, item: dict, owner_id: int, key: str):
        try:
            self.db.insert({'item': item, 'owner': str(owner_id)}, key)
            return True
        except Exception:
            return False

    async def fetch_public_tag(self, key: str):
        data = self.db.get(key)
        if data:
            return data.get('item'), data.get('owner')
        return None, None


class Global(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.func = AuxFunc()

    @commands.group(name='gtag', invoke_without_command=True)
    async def tag(self, ctx: commands.Context, tag: str):
        data, owner = await self.func.fetch_public_tag(key=tag)
        if data and owner:
            emd = discord.Embed(
                title=f'{data.get("name")}',
                description=f'{data.get("content")}',
                color=0xffffff
            )
            user = await self.bot.fetch_user(int(owner))
            emd.set_footer(text=f'Created by {user} | ( id: {owner} )')
            await ctx.send(embed=emd)
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='create')
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
                await ctx.send(f'Tag `{name}` already exists!')
        else:
            await ctx.send('Tag name must be at least 3 characters long.')

    @tag.command(name='raw')
    async def gtag_raw(self, ctx: commands.Context, name: str):
        data, _ = await self.func.fetch_public_tag(key=name)
        if data:
            emd = discord.Embed(description=f'{data}', color=0xffffff)
            await ctx.send(embed=emd)


def setup(bot: discord.Client):
    bot.add_cog(Global(bot))
