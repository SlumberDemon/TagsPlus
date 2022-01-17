import discord 
import dislash 
import datetime
from src.extras.func import *
from src.extras.views import *
from discord.ext import commands
from dislash import slash_command, Option, OptionType, SlashInteraction

class Slash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @dislash.slash_command(description='Tag commands')
    async def tag(self, inter: SlashInteraction):
        pass

    @tag.sub_command(description='Shows tag content', options=[Option('tag', 'Tag name', OptionType.STRING, True)])
    async def show(self, ctx, tag):
        data = await guild_get_tag(guild_id=ctx.guild.id, key=tag)
        if data:
            await ctx.send(data['item'][0]['content'])
        else:
            await ctx.send('Tag not found.')
    
    @tag.sub_command(description='Create tag', options=[Option('name', 'Tag name', OptionType.STRING, True), Option('content', 'Tag content', OptionType.STRING, True)])
    async def create(self, ctx, name, content):
        try:
            if 0 < len(name) >= 3:
                time = datetime.datetime.now()
                owner = f'{ctx.author.id}'
                await guild_create_tag(guild_id=ctx.guild.id, item=[{"owner": owner, "name": name, "content": content, "created_at": f'{time.day}/{time.month}/{time.year}'}], owner=owner, key=name)
                await ctx.send(f'Tag `{name}` successfully created.')
            else:
                await ctx.send('To `little` characters, please use three or more.')
        except Exception:
            await ctx.send('This tag already exists.')

    @tag.sub_command(description='Edit tag', options=[Option('name', 'Tag name', OptionType.STRING, True), Option('content', 'Tag content', OptionType.STRING, True)])
    async def edit(self, ctx, name, content):
        data = await guild_get_tag(guild_id=ctx.guild.id, key=name)
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

    @tag.sub_command(description='Delete tag', options=[Option('name', 'Tag name', OptionType.STRING, True)])
    async def delete(self, ctx, name):
        data = await guild_get_tag(guild_id=ctx.guild.id, key=name)
        if data and data['item']:
            owner = data['item'][0]['owner']
            view = Confirm(ctx)
            msg = await ctx.send(f'Want to delete `{name}` tag?', view=view)
            await view.wait()
            if view.value is None:
                await msg.edit('Tag deletion timed out.')
            elif view.value:
                if f'{ctx.author.id}' == f'{owner}':
                    await guild_delete_tag(guild_id=ctx.guild.id, key=name)
                    await msg.edit(f'Tag `{name}` successfully deleted.', view=None)
                else:
                    await msg.edit('You don\'t own this tag.', view=None)
            else:
                await msg.edit('Tag deletion cancelled.', view=None)
        else:
            await ctx.send('Tag not found.', view=None)

    @tag.sub_command(description='Raw tag', options=[Option('name', 'Tag name', OptionType.STRING, True)])
    async def raw(self, ctx, name):
        tag = await guild_get_tag(guild_id=ctx.guild.id, key=name)
        first_step = discord.utils.escape_markdown(tag['item'][0]['content'])
        data = (first_step.replace('<', '\\<'))
        embed = discord.Embed(description=f'\n{data}', colour=0xffffff)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Slash(bot))


