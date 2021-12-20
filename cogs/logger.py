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

class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def logger(self, title, desc, user, color, guild, image=None):
        print(f"log|N:{title.replace('**','')}| GID:{guild}")
        sixteenIntegerHex = int(color.replace("#", ""), 16)
        readableHex = int(hex(sixteenIntegerHex), 0)
        # print("converted to readable hex")
        time = datetime.datetime.now()  
        time = time.strftime(r"%x at %H:%M")
        # print("Set time")
        logEmbed = discord.Embed(title=f"{title}",description=desc, color=readableHex)
        if image!=None:
            logEmbed.set_thumbnail(url=image)
        # print("Set embed")
        logEmbed.timestamp = datetime.datetime.utcnow()
        logEmbed.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
        try:
            logEmbed.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)
        except:
            pass
        # print("set embed author/passed invalid user")
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        c = conn.cursor()
        # print("connected and cursored")
        command = f"select * from channels where type = 'logger' and guild_id = {guild}"
        # print(command)
        c.execute(command)
        # print("executed")
        results = c.fetchall()
        # print(results)
        # print(results[0][2])
        conn.commit()
        c.close()
        conn.close()
        # print("closed connection")
        # print(len(results))
        if len(results) != 0:
            channelsend = self.bot.get_channel(results[0][2])
        else:
            print(f'no log channel for guild {guild}')
            return
        # print(channelsend)
        await channelsend.send(embed=logEmbed)
        print("sent")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setlogger(self, ctx):
        if ctx.author.bot == True:
            return
        connect = self.bot.get_cog("Misc")
        # print('gotten connect')
        try:
            blist = await connect.checkblist(ctx, ctx.author)
        except:
            trace.print_exc()
        # print(f'connecting, {blist}')
        if blist is not None:
            if blist[1]=="global":
                # print('is global blist')
                await ctx.send(embed=blist[0])
                return
            else:
                pass
        else:
            pass
        print(f"Channel {ctx.channel.id} selected")
        channel = ctx.channel.id
        print(channel)
        guild = ctx.guild.id
        print(guild)
        conn = connect.connectdb()
        c = conn.cursor()
        print("Connected and cursored")
        command = f"select id from channels where guild_id={guild} and type='logger'"
        c.execute(command)
        print("executed")
        results = c.fetchall()
        results = str(results).replace(",)]", "")
        results = str(results).replace("[(", "")
        results = str(results).replace("[", "")
        results = str(results).replace("]", "")
        print(results)
        print(len(results))
        if len(results)==0:
            command5 = f"INSERT INTO channels(guild_id, channel_id, type) VALUES ({guild},{channel}, 'logger')"
            print(command5)
            c.execute(command5)
            print("executed")
        else:
            command5 = f"UPDATE channels SET channel_id={channel} where id = {results};" 
            command6 = f"UPDATE channels SET type='logger' where id = {results};"
            print(command5)
            print(command6)
            c.execute(command5)
            c.execute(command6)
            print("Logger set")
        conn.commit()
        c.close()
        conn.close()
        message=f"Chat <#{ctx.channel.id}> has been set as the log channel"
        print("message var set")
        await ctx.send(message)
        print("message sent")
        print("Channel succesfully set to logger")

    @setlogger.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.name}, You lack permission **Manage Server**")

def setup(bot):
    bot.add_cog(Logger(bot))