import discord
from discord import app_commands
from discord.ext import commands

class guild_leave_event(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(guild_leave_event(bot), guilds = [discord.Object(id=838814770537824378)])
