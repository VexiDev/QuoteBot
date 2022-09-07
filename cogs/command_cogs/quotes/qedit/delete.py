import discord
from discord import app_commands
from discord.ext import commands

class delete_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="delete", description="Removes a quote from a user")
    @app_commands.describe(user='The member you want to add a quote too (Cannot be a bot)')
    @app_commands.describe(quote='A part of the quote you wish to delete(Max 250 Characters)')
    async def delete(self, interaction: discord.Interaction, user: discord.User, quote: str):
        
        command = self.bot.get_cog('delquote')

        await command.delete(interaction, user, quote)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(delete_commands(bot), guilds = commands.Greedy[discord.Object])
