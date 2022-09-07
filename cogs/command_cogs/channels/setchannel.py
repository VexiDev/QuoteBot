import discord
from discord import app_commands
from discord.ext import commands

class setchannel_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    # @app_commands.command(name="setlogger", description="sets the log channel")
    async def setlogger(self, interaction: discord.Interaction, user: discord.User, quote: str):
        await interaction.response.send_message(f"Successfully added {quote} to {user}({user.id})")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(setchannel_commands(bot), guilds = [discord.Object(id=838814770537824378)])
