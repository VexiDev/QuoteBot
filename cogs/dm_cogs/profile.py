import discord
from discord import app_commands
from discord.ext import commands

class dmprofile(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(dmprofile(bot), guilds = [discord.Object(id=838814770537824378)])
