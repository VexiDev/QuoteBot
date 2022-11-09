import discord
from discord import app_commands
from discord.ext import commands

class quote_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="quote", description="Displays a random quote from a user")
    @app_commands.describe(user='Who you want to quote (Cannot be a bot)')
    @app_commands.describe(temporary='Automatically deletes message after 2 minutes')
    async def quote(self, interaction: discord.Interaction, user: discord.User, temporary: bool=False):
        
        command = self.bot.get_cog('quote')

        await command.quote(interaction, user, temporary)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(quote_commands(bot), guilds = commands.Greedy[discord.Object])
