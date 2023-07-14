import discord
from discord import app_commands
from discord.ext import commands

class setchannel_commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(name="setchannel", description="Set specific channels for QuoteBot messages")
    @app_commands.choices(type=[app_commands.Choice(name="Added Quotes", value="quotes")])
    @app_commands.describe(type='Select what messages will be dispalyed in that channel')
    @app_commands.describe(channel='Select a channel (leave blank to remove the channel)')
    async def setchannel(self, interaction: discord.Interaction, type: str, channel: discord.TextChannel = None):
        
        command = self.bot.get_cog('setchannel')

        await command.channel_set(interaction, type, channel)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(setchannel_commands(bot), guilds = commands.Greedy[discord.Object])
