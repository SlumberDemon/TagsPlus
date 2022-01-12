import discord, datetime
from discord.ext import commands
from src.extras.func import *
from src.extras.views import *

class Guild(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='tag', invoke_without_command=True)
    async def tag(self, ctx, tag):
        try:
            data = await guild_get_tag(guildId=ctx.guild.id, key=tag)
            await ctx.send(data['item'][0]['content'])
        except:
            await ctx.send('Tag not found.')

    @tag.command(name='create')
    async def tag_create(self, ctx, name, *, content:str):
        try:
            time = datetime.datetime.now() 
            await guild_create_tag(guildId=ctx.guild.id, item=[{"owner":f'{ctx.author.id}', "name":name, "content":content, "created_at":f'{time.day}/{time.month}/{time.year}'}], key=name)
            await ctx.send(f'Tag {name} successfully created.')
        except:
           await ctx.send('This tag already exists.')

    @tag.command(name='edit')
    async def tag_edit(self, ctx, tag, *, content:str):
        time = datetime.datetime.now() 
        try:
            data = await guild_get_tag(guildId=ctx.guild.id, key=tag)
            owner = data['item'][0]['owner']
            if f'{ctx.author.id}' == f'{owner}':
                await guild_edit_tag(guildId=ctx.guild.id, item=[{"owner":f'{ctx.author.id}', "name":tag, "content":content, "created_at":f'{time.day}/{time.month}/{time.year}'}], key=tag)
                await ctx.send(f'Tag {tag} successfully edited.')
            else:
                await ctx.send('You don\'t own this tag.', view=None)
        except:
            await ctx.send('Tag not found.')


    @tag.command(name='delete')
    async def tag_delete(self, ctx, tag):
        try:
            data = await guild_get_tag(guildId=ctx.guild.id, key=tag)
            owner = data['item'][0]['owner']
            view = Confirm(ctx)
            msg = await ctx.send(f'Want to delete {tag} tag?', view=view)
            await view.wait()
            if view.value is None:
                await ctx.send('Tag deletion timed out.')
            elif view.value:
                if f'{ctx.author.id}' == f'{owner}':
                    await guild_delete_tag(guildId=ctx.guild.id, key=tag)
                    await msg.edit(f'Tag {tag} successfully deleted.', view=None)
                else:
                    await msg.edit('You don\'t own this tag.', view=None)
            else:
                await msg.edit('Tag deletion cancelled.', view=None)
        except:
            await msg.edit('Tag not found.', view=None)

    @tag.command(name='raw')
    async def tag_raw(self, ctx, tag):
        tag = await guild_get_tag(guildId=ctx.guild.id, key=tag)
        first_step = discord.utils.escape_markdown(tag['item'][0]['content'])
        await ctx.send(first_step.replace('<', '\\<'))

    @tag.command(name='info')
    async def tag_info(self, ctx, tag):
        try:
            info = await guild_get_tag(guildId=ctx.guild.id, key=tag)
            em = discord.Embed(title=info['item'][0]['name'], colour=0xffffff)
            em.add_field(name='Content', value=info['item'][0]['content'], inline=False)
            em.add_field(name='Owner', value='<@' + info['item'][0]['owner'] + '>', inline=True)
            em.add_field(name='Created at', value=info['item'][0]['created_at'], inline=True)
            await ctx.send(embed=em)
        except:
            await ctx.send('Tag not found.')

def setup(bot):
    bot.add_cog(Guild(bot))
    