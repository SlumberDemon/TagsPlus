import discord
from discord.ext import commands

class Confirm(discord.ui.View):
    def __init__(self, context: commands.Context):
        super().__init__()
        self.value = None
        self.ctx = context

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            self.value = True
            self.stop()
        else:
            await interaction.response.send_message('You are not allowed to control this message', ephemeral=True)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            self.value = False
            self.stop()
        else:
            await interaction.response.send_message('You are not allowed to control this message', ephemeral=True)