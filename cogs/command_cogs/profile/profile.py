import discord
from discord import app_commands
from discord.ext import commands

class profile_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="profile", description="Displays a user's QuoteBot Profile")
    @app_commands.describe(user='Who\'s profile you want to view (Cannot be a bot)')
    @app_commands.describe(hidden='Hides the message from everyone but you')
    async def profile(self, interaction: discord.Interaction, user: discord.User, hidden: bool=False):
        
        command = self.bot.get_cog('profile')

        await command.profile(interaction, user, hidden)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(profile_commands(bot), guilds = commands.Greedy[discord.Object])
