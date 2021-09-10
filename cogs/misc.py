import discord
from discord.ext import commands
from  builtins import any
from discord import Intents
import requests
import os
import random
import asyncio
import datetime
import psycopg2

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("tested")

    def connectdb(self):
        conn = psycopg2.connect(        
        host="address",
        database="database name",
        user="user",
        password="pass") 
        return(conn)

    @commands.command()
    async def invite(self,ctx):
            await ctx.send("https://discord.com/api/oauth2/authorize?client_id=814379239930331157&permissions=8&scope=bot")
    

    @commands.command()
    async def info(self, ctx):
        conn = self.connectdb()
        c = conn.cursor()
        command = f"SELECT version FROM version WHERE id = 1"
        print(command)
        c.execute(command)
        ver_results = c.fetchall()
        command2 = f"SELECT count(distinct qid) FROM quotes"
        print(command2)
        c.execute(command2)
        results_total_quotes = c.fetchall()
        command3 = f"SELECT COUNT(DISTINCT uid) FROM quotes"
        print(command3)
        c.execute(command3)
        results_total_users = c.fetchall()
        conn.close()
        infoEmbed = discord.Embed(title=f"QuoteBot Info", description=f"\nCurrent Version: **{ver_results}**\nTotal Quotes logged: **{results_total_quotes}**\nTotal unique users: **{results_total_users}**", color=0xf5e642)
        await ctx.send(embed=infoEmbed)

def setup(bot):
    bot.add_cog(Misc(bot))