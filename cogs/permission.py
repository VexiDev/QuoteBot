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

class Permission(commands.Cog):
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
    @commands.has_permissions(administrator=True)
    async def permission(self, ctx, action, user: discord.User, *, permission=""):
        if action == "add":
            conn = psycopg2.connect(
            host="adwess",
            database="databasename",
            user="username",
            password="password here")
            c = conn.cursor()
            command = f"insert into permission(uid,perm) values ({user.id},'{permission}')"
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            conn.close()
            await ctx.send(f"Permission {permission} added to <@{user.id}>")
            await self.logger(command=f"**Gave permision** {permission} to {user.name}", user=ctx.author, channel=ctx.channel, color="#0ff231", guild=ctx.message.guild.id)

        elif action == "remove":
            conn = psycopg2.connect(
            host="adwess",
            database="databasename",
            user="username",
            password="password here")
            c = conn.cursor()
            command = f"delete from permission where perm = '{permission}' and uid = {user.id}"
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            conn.close()
            await ctx.send(f"Permission {permission} removed to <@{user.id}>")
            await self.logger(command=f"**Removed permision** {permission} from {user.name}", user=ctx.author, channel=ctx.channel, color="#f20f0f", guild=ctx.message.guild.id)

        elif action == "show":
            conn = psycopg2.connect(
            host="adwess",
            database="databasename",
            user="username",
            password="password here")
            c = conn.cursor()
            command = f"SELECT perm FROM permission WHERE uid = {user.id}"
            print(command)
            c.execute(command)
            results = c.fetchall()
            conn.commit()
            c.close()
            conn.close()
            embedVar7 = discord.Embed(title=f"Permissions for {user.name}:", color=0x00ff00)
            print(results)
            for i in range(len(results)): 
                results[i] = str(results[i]).replace("('", "")
                results[i] = str(results[i]).replace("',)", "")
            for i in range(len(results)):
                embedVar7.add_field(name=f"{results[i]}", value=f"allows use of the {results[i]} command", inline=False)
            await ctx.send(embed=embedVar7)
            

    @permission.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are not an administrator!")
            await self.logger(command=f"Tried to use **permission** but lacks discord ***Administrator*** permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
    

def setup(bot):
    bot.add_cog(Permission(bot))
