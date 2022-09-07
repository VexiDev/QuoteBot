import discord
import topgg
from discord import app_commands
from discord.ext import commands

class updater(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @tasks.loop(hours=12)
    async def update_stats(self):
        try:
            await self.bot.topggpy.post_guild_count()
            print(f"Posted server count ({self.bot.topggpy.guild_count})")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(updater(bot), guilds = [discord.Object(id=838814770537824378)])
