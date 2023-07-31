import discord
from discord import app_commands
from discord.ext import commands

class scan_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="scan", description="Scan message history for quotes")
    @app_commands.describe(target_channel='Select a channel to scan')
    @app_commands.describe(destination_channel='Select a channel to send quotes too')
    async def scancommand(self, interaction: discord.Interaction, target_channel: discord.TextChannel, destination_channel: discord.TextChannel):
        
        command = self.bot.get_cog('scan')

        await command.quote_scan(interaction, target_channel, destination_channel)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(scan_commands(bot), guilds = commands.Greedy[discord.Object])
