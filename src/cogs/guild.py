import discord
import datetime
from discord.ext import commands
from src.extras.views import Confirm
from src.extras.func import guild_create_tag, guild_fetch_user, guild_edit_tag, guild_delete_tag, guild_get_tag


class Guild(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def tag(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        try:
            await ctx.send(data['item'][0]['content'])
        except:
            await ctx.send('Tag not found.')

    @tag.command(name='create')
    async def tag_create(self, ctx, name, *, content: str=None):
        try:
            check = await guild_get_tag(guild_id=ctx.guild.id, tag=name)
            if check['name'] == name:
                await ctx.send('This tag already exists.')
            elif check['key'] == name:
                await ctx.send('Tags cannot use another tags ID as name.')
            elif 0 < len(name) >= 3:
                await ctx.send('To `little` characters, please use three or more.')
        except:
            if content == None:
                await ctx.send('Missing tag content.')
            else:
                time = datetime.datetime.utcnow()
                owner = f'{ctx.author.id}'
                await guild_create_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": name, "content": content, "created_at": str(time)}], owner=owner, name=name)
                await ctx.send(f'Tag `{name}` successfully created.')

    @tag.command(name='edit')
    async def edit(self, ctx, name, *, content: str):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=name)
        if data:
            owner = data['item'][0]['owner']
            if f'{ctx.author.id}' == f'{owner}':
                time = datetime.datetime.utcnow()
                await guild_edit_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": name, "content": content, "created_at": str(time)}], owner=owner, name=name)
                await ctx.send(f'Tag `{name}` successfully edited.')
            else:
                await ctx.send('You don\'t own this tag.', view=None)
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='delete')
    async def tag_delete(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        if data:
            owner = data['owner']
            view = Confirm(ctx)
            msg = await ctx.send(f'Want to delete `{data["name"]}` tag?', view=view)
            await view.wait()
            if view.value is None:
                await msg.edit('Tag deletion timed out.')
            elif view.value:
                if f'{ctx.author.id}' == f'{owner}':
                    await guild_delete_tag(guild_id=ctx.guild.id, key=data['key'])
                    await msg.edit(f'Tag `{data["name"]}` successfully deleted.', view=None)
                else:
                    await msg.edit('You don\'t own this tag.', view=None)
            else:
                await msg.edit('Tag deletion cancelled.', view=None)
        else:
            await ctx.send('Tag not found.', view=None)

    @tag.command(name='raw')
    async def tag_raw(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        if data:
            new = discord.utils.escape_markdown(data['item'][0]['content'])
            text = (new.replace('<', '\\<'))
            embed = discord.Embed(description=f'{text}', colour=0xffffff)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='info')
    async def tag_info(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        if data:
            info = data['item'][0]
            time = discord.utils.format_dt(datetime.datetime.fromisoformat(info['created_at']), style='f')
            em = discord.Embed(title=info['name'], colour=0xffffff)
            em.add_field(name='Content', value=info['content'], inline=False)
            em.add_field(name='Owner', value='<@' + info['owner'] + '>', inline=True)
            em.add_field(name='Created at / Last edit', value=time, inline=True)
            await ctx.send(embed=em)
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='all')
    async def tag_all(self, ctx):
        msg = await ctx.send('Fetching tags...')
        tags = ''
        for user in ctx.guild.members:
            data = await guild_fetch_user(guild_id=ctx.guild.id, owner=f'{user.id}')
            if data.items:
                for item in data.items:
                    tags+=' ' + item['name'] + ' (ID: ' + item['key'] + ')' + '\n'
                    await msg.edit(f'Chunking **{data.count}** item(s) continuing to fetch...')
            else:
                pass
        em = discord.Embed(description=tags, colour=0xffffff)
        em.set_author(name='Guild Tag(s)', icon_url=ctx.guild.icon.url)
        await msg.edit(content=None, embed=em)

    @commands.command(name='tags')
    async def user_tags(self, ctx, user: discord.User=None):
        user = ctx.author if not user else user
        data = await guild_fetch_user(guild_id=ctx.guild.id, owner=f'{user.id}')
        tags = ''
        for item in data.items:
            tags+=' ' + item['name'] + ' (ID: ' + item['key'] + ') \n'
        em = discord.Embed(description=tags, colour=0xffffff)
        em.set_author(name=user.display_name, icon_url=user.avatar.url)
        em.set_footer(text=f'{data.count} Tag(s)')
        await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(Guild(bot))
