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
        if data:
            await ctx.send(data['item'][0]['content'])
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='create')
    async def tag_create(self, ctx, name, *, content: str):
        try:
            if 0 < len(name) >= 3:
                time = datetime.datetime.now()
                owner = f'{ctx.author.id}'
                tag_name = name.replace(' ', '_')
                await guild_create_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": tag_name, "content": content, "created_at": f'{time.day}/{time.month}/{time.year}'}], owner=owner, name=tag_name)
                await ctx.send(f'Tag `{name}` successfully created.')
            else:
                await ctx.send('To `little` characters, please use three or more.')
        except Exception:
            await ctx.send('This tag already exists or you are using a tag ID as a name.')

    @tag.command(name='edit')
    async def edit(self, ctx, name, *, content: str):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=name)
        if data and data['item']:
            owner = data['item'][0]['owner']
            if f'{ctx.author.id}' == f'{owner}':
                time = datetime.datetime.now()
                await guild_edit_tag(guild_id=ctx.guild.id, item=[
                    {"owner": f'{ctx.author.id}', "name": name, "content": content,
                     "created_at": f'{time.day}/{time.month}/{time.year}'}], key=name)
                await ctx.send(f'Tag `{name}` successfully edited.')
            else:
                await ctx.send('You don\'t own this tag.', view=None)
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='delete')
    async def tag_delete(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        if data and data['item']:
            owner = data['item'][0]['owner']
            view = Confirm(ctx)
            msg = await ctx.send(f'Want to delete `{tag}` tag?', view=view)
            await view.wait()
            if view.value is None:
                await msg.edit('Tag deletion timed out.')
            elif view.value:
                if f'{ctx.author.id}' == f'{owner}':
                    await guild_delete_tag(guild_id=ctx.guild.id, key=tag)
                    await msg.edit(f'Tag `{tag}` successfully deleted.', view=None)
                else:
                    await msg.edit('You don\'t own this tag.', view=None)
            else:
                await msg.edit('Tag deletion cancelled.', view=None)
        else:
            await ctx.send('Tag not found.', view=None)

    @tag.command(name='raw')
    async def tag_raw(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        if tag:
            first_step = discord.utils.escape_markdown(tag['item'][0]['content'])
            data = (first_step.replace('<', '\\<'))
            embed = discord.Embed(description=f'\n{data}', colour=0xffffff)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='info')
    async def tag_info(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, tag=tag)
        if data and data['item']:
            info = data['item'][0]
            em = discord.Embed(title=info['name'], colour=0xffffff)
            em.add_field(name='Content', value=info['content'], inline=False)
            em.add_field(name='Owner', value='<@' + info['owner'] + '>', inline=True)
            em.add_field(name='Created at', value=info['created_at'], inline=True)
            await ctx.send(embed=em)
        else:
            await ctx.send('Tag not found.')

    @tag.command(name='all')
    async def tag_all(self, ctx):
        tags = ''
        for user in ctx.guild.members:
            data = await guild_fetch_user(guild_id=ctx.guild.id, owner=f'{user.id}')
            if data.items:
                for item in data.items:
                    tags+=' ' + item['name'] + ' (ID: ' + item['key'] + ')' + '\n'
            else:
                pass
        em = discord.Embed(description=tags, colour=0xffffff)
        em.set_author(name='Guild Tag(s)', icon_url=ctx.guild.icon.url)
        await ctx.send(embed=em)

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
