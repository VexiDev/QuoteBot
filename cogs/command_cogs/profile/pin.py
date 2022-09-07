import discord
from discord import app_commands
from discord.ext import commands

class pin_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="pin", description="Pins a quote on your public profile")
    @app_commands.describe(hidden='Hides the message from everyone but you')
    @app_commands.describe(quote='A section of the quote you want to pin, quotebot will autofill (Max 250 Characters)')
    async def pin(self, interaction: discord.Interaction, quote: app_commands.Range[str, 1, 250], hidden: bool=False):
        
        command = self.bot.get_cog('edit_pin')

        await command.pin(interaction, quote, hidden)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(pin_commands(bot), guilds = commands.Greedy[discord.Object])
