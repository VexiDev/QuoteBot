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
        host="ec2-107-20-153-39.compute-1.amazonaws.com",
        database="d54rrbkoagiuqg",
        user="bcqrzmrdonxkml",
        password="006986da51bca028a4af7404fde38e18c9f8a6208b495187b93d4744632b652d") 
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
        guilds = len(self.bot.guilds)
        final_ver_results = str(ver_results[0]).replace("('(1,", "").replace(")',)", "")
        infoEmbed = discord.Embed(title=f"QuoteBot Info", description=f"\nCurrent Version: **{final_ver_results}**\nTotal Quotes logged: **{str(results_total_quotes[0]).replace('(', '').replace(',)','')}**\nTotal unique users: **{str(results_total_users[0]).replace('(', '').replace(',)','')}**\nTotal Unique Servers: **{guilds}**", color=0xf5e642)
        await ctx.send(embed=infoEmbed)

def setup(bot):
    bot.add_cog(Misc(bot))