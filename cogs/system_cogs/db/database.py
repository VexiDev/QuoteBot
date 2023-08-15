import discord
import psycopg2
from discord import app_commands
from discord.ext import commands

class database(commands.Cog):
    def __init__(self, bot: commands.Bot, env_vars: dict) -> None:
        self.bot = bot
        self.env_vars = env_vars

    def connect(self):
        conn = psycopg2.connect(        
        host=f"{self.env_vars['db_host']}",
        database=f"{self.env_vars['db_name']}",
        user=f"{self.env_vars['db_user']}",
        password=f"{self.env_vars['db_pass']}",
        sslmode='require')
        return(conn)   

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(database(bot), guilds = commands.Greedy[discord.Object])
