import discord
from discord import app_commands
from discord.ext import commands

class help_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="A help menu for QuoteBot's commands and features")
    async def help(self, interaction: discord.Interaction):
        
        #this menu is always hidden
        hidden=True
        
        command = self.bot.get_cog('help_me')

        await command.help_menu(interaction, hidden)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(help_commands(bot), guilds = commands.Greedy[discord.Object])
