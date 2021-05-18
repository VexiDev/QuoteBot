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
    async def purge(self, ctx, limit: int):
        print("Started purge")
        await ctx.channel.purge(limit=limit+1)
        print("porged")
        log = self.bot.get_cog("Logger")
        await log.logger(command=f"**Purged** {limit} messages from {ctx.channel}", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
        print("logged")

    @commands.command()
    async def fight(self, ctx, user1: discord.User, user2: discord.User):
        # await ctx.send("The fight command is currently disabled")
        randnum = random.randint(1, 6)
        print(randnum)
        if randnum == 3 or randnum == 5 or randnum == 1:
            await ctx.send(f"<@{user1.id}> wins!")
        elif randnum == 4 or randnum == 2 or randnum == 6:
            await ctx.send(f"<@{user2.id}> wins!")

    @commands.command()
    async def geraltcock(self,ctx):
        author = ctx.message.author
        conn = psycopg2.connect(
        host="ec2-107-20-153-39.compute-1.amazonaws.com",
        database="d54rrbkoagiuqg",
        user="bcqrzmrdonxkml",
        password="006986da51bca028a4af7404fde38e18c9f8a6208b495187b93d4744632b652d")
        c = conn.cursor()
        command = f"SELECT perm FROM permission WHERE uid = {author.id}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        print(results)
        conn.commit()
        c.close()
        conn.close()
        for i in range(len(results)): 
            results[i] = str(results[i]).replace("('", "")
            results[i] = str(results[i]).replace("',)", "")
        print(results)
        if ('geraltcock' in results):
            await ctx.send("https://geralt.big-cock.club/3JYHWYic")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Used **geraltcock** to bless their eyes", user=ctx.author, channel=ctx.channel, color="#42f5b3", guild=ctx.message.guild.id)
        else: 
            await ctx.send("You lack permission to use this command.")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to use **geraltcock** but lacks permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
        
        
    @commands.command()
    async def sleeptest(self,ctx, time):
        message = await ctx.send("this is a test")
        await asyncio.sleep(int(time))
        await message.delete()
        await ctx.message.delete()
        time1 = str(time)
        log = self.bot.get_cog("Logger")
        await log.logger(command=f"Used **sleeptest** for {time1} second(s)", user=ctx.author, channel=ctx.channel, color="#42f5b3", guild=ctx.message.guild.id)

    @commands.command()
    async def info(self, ctx):
        conn = psycopg2.connect(
        host="adwess",
        database="databasename",
        user="username",
        password="password here")
        c = conn.cursor()
        command = f"SELECT version FROM version WHERE id = 1"
        print(command)
        c.execute(command)
        results = c.fetchall()
        results = str(results).replace("(", "")
        results = str(results).replace(",)", "")
        results = str(results).replace("]", "")
        results = str(results).replace("[", "")
        results = str(results).replace("'1,", "")
        results = str(results).replace(")'", "")
        print(results)
        conn.commit()
        c.close()
        conn.close()
        command2 = f"SELECT * FROM quotes"
        conn = psycopg2.connect(
        host="adwess",
        database="databasename",
        user="username",
        password="password here")
        c = conn.cursor()
        print(command2)
        c.execute(command2)
        results2 = c.fetchall()
        results2 = len(results2)
        conn.commit()
        conn = psycopg2.connect(
        host="adwess",
        database="databasename",
        user="username",
        password="password here")
        c = conn.cursor()
        command3 = f"SELECT COUNT(DISTINCT uid) FROM quotes"
        print(command3)
        c.execute(command3)
        results3 = c.fetchall()
        results3 = str(results3).replace("(", "")
        results3 = str(results3).replace(",)", "")
        results3 = str(results3).replace("]", "")
        results3 = str(results3).replace("[", "")
        conn.commit()
        conn.close()
        infoEmbed = discordembed=discord.Embed(title=f"QuoteBot Info", description=f"\nCurrent Version: **{results}**\nTotal Quotes logged: **{results2}**\nTotal unique users: **{results3}**", color=0xf5e642)
        await ctx.send(embed=infoEmbed)

def setup(bot):
    bot.add_cog(Misc(bot))
