import discord
from discord import app_commands
from discord.ext import commands

class lookup_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @app_commands.command(name="lookup", description="looks up global info on a user/server")
    @app_commands.describe(type='Select if you want to get the info of a user or server')
    @app_commands.describe(id='The ID of the user or server')
    @app_commands.describe(hidden='Hides this interaction from everyone but you')
    @app_commands.choices(type=[app_commands.Choice(name="User", value="1"),app_commands.Choice(name="Server", value="2"),])
    async def lookup(self, interaction: discord.Interaction, type: str, id: str, hidden: bool=False):
        
        command = self.bot.get_cog('lookup')

        await command.lookup(interaction, type, id)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(lookup_commands(bot), guilds = [discord.Object(id=838814770537824378)])
