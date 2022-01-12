import discord, os, datetime
from typing import Union
from deta import Deta
from discord.ext import commands


class AuxFunc:

    def __init__(self):
        self.deta = Deta(os.getenv('DETA'))
        self.db = self.deta.Base('PUBLIC_TAGS')

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
        previous = await self.func.fetch_public_tag(key=name)
        if previous:
            await ctx.send('Merging with previous tags')
            item = previous.append({
                "owner": f'{ctx.author.id}',
                "name": name,
                "content": content,
                "created_at": f'{time.day}/{time.month}/{time.year}'
            })
            await self.func.push_public_tag(item=item, key=name)

        else:
            await ctx.send(f'Tag `{name}` successfully created.')
            item = [{
                "owner": f'{ctx.author.id}',
                "name": name,
                "content": content,
                "created_at": f'{time.day}/{time.month}/{time.year}'
            }]
            await self.func.push_public_tag(item=item, key=name)


def setup(bot: discord.Client):
    bot.add_cog(Global(bot))
