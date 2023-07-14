import discord
from discord import app_commands
from discord.ext import commands

class lookup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def lookup(self, interaction: discord.Interaction, type: str, id: str, hidden=False):

        slook = self.bot.get_cog("server_lookup")
        ulook = self.bot.get_cog("user_lookup")

        if type == "1":
            user = await self.bot.fetch_user(int(id))
            await ulook.user_lookup(interaction, user, hidden)
        elif type == "2":
            await slook.server_lookup(interaction, int(id), hidden)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(lookup(bot), guilds = [discord.Object(id=838814770537824378)])
