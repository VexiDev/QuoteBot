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

class Dmsys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def dm(self, ctx, user: discord.User, *, message=None):
        print("dm func started")
        # author = ctx.message.author
        # print("set author var")
        conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password")
        print("Successfully connected to postgresql database")
        c = conn.cursor()
        print("cursored")
        command = f"SELECT * FROM permission WHERE uid = {ctx.author.id} and guild_id = {ctx.guild.id}"
        print("set command")
        print(command)
        c.execute(command)
        print("executed")
        results = c.fetchall()
        print("results gathered")
        print(results)
        conn.commit()
        c.close()
        conn.close()
        permcount = 0
        print("closed connection")
        print(results)
        for perm in results:
            if(perm[2] == 'dm'):
                print("user has permission")
                message = message or "wee woo"
                print("set message")
                await user.send(message)
                print("sent message")
                log = self.bot.get_cog("Logger")
                await log.logger(command=f"Used **dm** - sent to {user}\n message: \"{message}\"", user=ctx.author, channel=ctx.channel, color="#ff40e2", guild=ctx.message.guild.id)
                print("logged")
            else: 
                permcount = permcount+1
                
            if permcount == len(results):
                print("user doesnt have permission")
                await ctx.send("You lack permission to use this command.")
                log = self.bot.get_cog("Logger")
                await log.logger(command=f"Tried to use **dm** but lacks permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                print("logged")

    @commands.command()
    async def dmspam(self, ctx, user: discord.User, amount=0,*, message=""):
        author = ctx.message.author
        conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password")
        c = conn.cursor()
        command = f"SELECT * FROM permission WHERE uid = {author.id} and {ctx.guild.id}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        print(results)
        conn.commit()
        conn.close()
        print(results)
        for perm in results:
            if (perm[2] == 'dmspam'):
                print("has permission")
                await ctx.send(f"Queued dmspam to user {user}")
                message = message or "uwu heyyy"
                r = amount or 5
                await asyncio.sleep(2)
                log = self.bot.get_cog("Logger")
                await log.logger(command=f"Used **dmspam** for {amount} messages to {user} \nmessage: \"{message}\"", user=ctx.author, channel=ctx.channel, color="##ff40e2", guild=ctx.message.guild.id)
                await ctx.send("Started")
                for i in range(r):
                    await user.send(message)
                    
            else: 
                await ctx.send("You lack permission to use this command.")
                log = self.bot.get_cog("Logger")
                await log.logger(command=f"Tried to use **dmspam** but lacks permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                


def setup(bot):
    bot.add_cog(Dmsys(bot))
