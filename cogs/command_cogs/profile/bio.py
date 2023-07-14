import discord
from discord import app_commands
from discord.ext import commands

class bio_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="bio", description="Changes the bio on your public profile")
    @app_commands.describe(bio='What you want your new bio to be')
    @app_commands.describe(hidden='Hides this interaction from everyone but you')
    async def bio(self, interaction: discord.Interaction, bio: app_commands.Range[str, 1, 250], hidden: bool=False):
        
        command = self.bot.get_cog('edit_bio')

        await command.bio(interaction, bio, hidden)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(bio_commands(bot), guilds = commands.Greedy[discord.Object])
