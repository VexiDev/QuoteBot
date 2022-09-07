import discord
from discord import app_commands
from discord.ext import commands

class quote_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="quote", description="Displays a random quote from a user")
    async def quote(self, interaction: discord.Interaction, user: discord.User):
        
        command = self.bot.get_cog('quote')

        await command.quote(interaction, user)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(quote_commands(bot), guilds = commands.Greedy[discord.Object])
