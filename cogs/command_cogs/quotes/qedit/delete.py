import discord
from discord import app_commands
from discord.ext import commands

class delete_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="delete", description="Deletes a quote from a user")
    @app_commands.describe(user='The member you want to remove a quote from (Cannot be a bot)')
    @app_commands.describe(quote='A part of the quote you want to delete')
    async def delete(self, interaction: discord.Interaction, user: discord.User, quote: app_commands.Range[str, 1, 250]):
        
        command = self.bot.get_cog('delquote')

        await command.delete(interaction, user, quote)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(delete_commands(bot), guilds = commands.Greedy[discord.Object])
