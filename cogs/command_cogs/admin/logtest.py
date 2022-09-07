import discord
import datetime
from discord import app_commands
from discord.ext import commands

class test_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # @app_commands.command(name="logtest", description="Runs a fake log request")
    async def lag(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Running fake log request")
        log = self.bot.get_cog("logger")
        await log.logger(title=f"**Test Log**", desc=f'**"QUOTE"**\n\n**From:** USER\n**By:** USER*', user=interaction.user, color="#DE6363", guild=interaction.guild.id, image=interaction.user.display_avatar.url)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(test_commands(bot), guilds = [discord.Object(id=838814770537824378)])
