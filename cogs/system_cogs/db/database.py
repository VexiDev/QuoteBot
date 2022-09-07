import discord
import psycopg2
from discord import app_commands
from discord.ext import commands

class database(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def connect(self):
        conn = psycopg2.connect(        
        host="ec2-52-72-60-116.compute-1.amazonaws.com",
        database="datps9doutonos",
        user="u4k1sd87l5j3gd",
        password="pfed15ef5520e45dccea4f5ff6e262cbbc88c25494784d3841b546770dd2e4b37", 
        sslmode='require')
        return(conn)   

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(database(bot), guilds = commands.Greedy[discord.Object])
