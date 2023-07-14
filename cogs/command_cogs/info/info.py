import discord
from discord import app_commands
from discord.ext import commands

class info_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="info", description="Display a info menu for quotebot")
    async def info(self, interaction: discord.Interaction):
        
        #this menu is always hidden
        hidden=True
        
        command = self.bot.get_cog('info')

        await command.info_menu(interaction, hidden)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(info_commands(bot), guilds = commands.Greedy[discord.Object])
