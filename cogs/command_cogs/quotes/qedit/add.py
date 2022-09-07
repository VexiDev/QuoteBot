import discord
from discord import app_commands
from discord.ext import commands

class add_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="add", description="Adds a quote to a user")
    @app_commands.describe(user='The member you want to add a quote too (Cannot be a bot)')
    @app_commands.describe(quote='The quote you wish to add (Max 250 Characters)')
    async def add(self, interaction: discord.Interaction, user: discord.User, quote: app_commands.Range[str, 1, 250]):
        
        command = self.bot.get_cog('addquote')

        await command.add(interaction, user, quote)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(add_commands(bot), guilds = commands.Greedy[discord.Object])
