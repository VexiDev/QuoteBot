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

    async def logger(self, command, user, channel, color, guild,):
        print("Started log")
        channelsend = self.bot.get_channel(839963726941519873)
        print("set log channel")
        sixteenIntegerHex = int(color.replace("#", ""), 16)
        readableHex = int(hex(sixteenIntegerHex), 0)
        print("converted to readable hex")
        time = datetime.datetime.now()  
        time = time.strftime(r"%x at %H:%M")
        print("Set time")
        print(command)
        logEmbed = discord.Embed(title=f"{user}", description=f"{command} \n\n <#{channel.id}> | guildID: {guild} | {time}", color=readableHex)
        print("Set embed")
        print(user.avatar_url)
        logEmbed.set_thumbnail(url=user.avatar_url)
        print("set embed thumbnail")
        await channelsend.send(embed=logEmbed)
        print("sent")
        print(f"{user} | {command} | channelID: {channel.id} | guildID: {guild} | {time}")


    @commands.command()
    async def dm(self, ctx, user: discord.User, *, message=None):
        print("dm func started")
        # author = ctx.message.author
        # print("set author var")
        conn = psycopg2.connect(
        host="adwess",
        database="databasename",
        user="username",
        password="password here")
        print("Successfully connected to postgresql database")
        c = conn.cursor()
        print("cursored")
        command = f"SELECT perm FROM permission WHERE uid = {ctx.author.id}"
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
        print("closed connection")
        for i in range(len(results)): 
            results[i] = str(results[i]).replace("('", "")
            results[i] = str(results[i]).replace("',)", "")
        print(results)
        if ('dm' in results):
            print("user has permission")
            message = message or "wee woo"
            print("set message")
            await user.send(message)
            print("sent message")
            await logger(command=f"Used **dm** - sent to {user}\n message: \"{message}\"", user=ctx.author, channel=ctx.channel, color="#ff40e2", guild=ctx.message.guild.id)
            print("logged")
        else: 
            print("user doesnt have permission")
            await ctx.send("You lack permission to use this command.")
            await logger(command=f"Tried to use **dm** but lacks permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
            print("logged")

    @commands.command()
    async def dmspam(self, ctx, user: discord.User, amount=0,*, message=""):
        author = ctx.message.author
        conn = psycopg2.connect(
        host="adwess",
        database="databasename",
        user="username",
        password="password here")
        c = conn.cursor()
        command = f"SELECT perm FROM permission WHERE uid = {author.id}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        print(results)
        conn.commit()
        conn.close()
        for i in range(len(results)): 
            results[i] = str(results[i]).replace("('", "")
            results[i] = str(results[i]).replace("',)", "")
        print(results)
        if ('dmspam' in results):
            await ctx.send(f"Queued dmspam to user {user}")
            message = message or "uwu heyyy"
            r = amount or 5
            await asyncio.sleep(2)
            await logger(command=f"Used **dmspam** for {amount} messages to {user} \nmessage: \"{message}\"", user=ctx.author, channel=ctx.channel, color="##ff40e2", guild=ctx.message.guild.id)
            await ctx.send("Started")
            for i in range(r):
                await user.send(message)
                
        else: 
            await ctx.send("You lack permission to use this command.")
            await logger(command=f"Tried to use **dmspam** but lacks permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
            


def setup(bot):
    bot.add_cog(Dmsys(bot))
