import discord
from discord import app_commands
from discord.ext import commands

class settings_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="settings", description="Modify QuoteBot settings for your server") 
    async def settings(self, interaction: discord.Interaction):
        
        command = self.bot.get_cog('server_settings')

        await command.edit_server_settings(interaction)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(settings_commands(bot), guilds = commands.Greedy[discord.Object])
