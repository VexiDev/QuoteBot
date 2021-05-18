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

class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def setupdater(self, ctx):
        print(f"Channel {ctx.channel.id} selected")
        channel = ctx.channel.id
        print(channel)
        guild = ctx.guild.id
        print(guild)
        conn = psycopg2.connect(
        host="adwess",
        database="databasename",
        user="username",
        password="password here")
        c = conn.cursor()
        print("Connected and cursored")
        command = f"select id from channels where guild_id={guild} and type='update'"
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
            command5 = f"INSERT INTO channels(guild_id, channel_id, type) VALUES ({guild},{channel}, 'update')"
            print(command5)
            c.execute(command5)
            print("executed")
        else:
            command5 = f"UPDATE channels SET channel_id={channel} where id = {results};" 
            command6 = f"UPDATE channels SET type='update' where id = {results};"
            print(command5)
            print(command6)
            c.execute(command5)
            c.execute(command6)
        conn.commit()
        c.close()
        conn.close()
        message=f"Chat <#{ctx.channel.id}> has been set as the update channel"
        await ctx.send(message)
        print("Channel succesfully logged")
    
    @commands.command()
    async def update(self, ctx, level="",*, updated=""):
        print(ctx.author.id)
        if ctx.author.id == 274213987514580993:    
            await ctx.message.delete()
            if level=="major":
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
                print(results)
                results = str(results).replace("[('(1,", "")
                results = str(results).replace(")',)]", "")
                print(results)
                conn.commit()
                c.close()
                conn.close()
                results = float(results)+1
                print(results)
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command = f"UPDATE version SET ver='{results}' WHERE id=1"
                print(command)
                c.execute(command)
                conn.commit()
                c.close()
                conn.close()
                print("executed")
                #-------get updater channel---------
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command2 = f"select * from channels where type = 'update'"
                print(command2)
                c.execute(command2)
                results2 = c.fetchall()
                print(results2)
                conn.commit()
                c.close()
                conn.close()
                #------------------------------------
                updateEmbed = discord.Embed(title=f"Updated to v{results}", description=f"{ctx.author.name} updated QuoteBot", color=0xf5e642)
                print("created embed")
                updateEmbed.add_field(name="Changelog:", value=f"{updated}",inline=False)
                print("added changelog")
                updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
                print("added image")
                print(f"length of results = {len(results2)}")
                for total in range(len(results2)):
                    sendchannel = self.bot.get_channel(results2[total][2])
                    print(sendchannel)
                    print(results2[total][2])
                    await sendchannel.send(embed=updateEmbed)
                
            if level=="minor":
                conn = psycopg2.connect(
                host="ec2-107-20-153-39.compute-1.amazonaws.com",
                database="d54rrbkoagiuqg",
                user="bcqrzmrdonxkml",
                password="006986da51bca028a4af7404fde38e18c9f8a6208b495187b93d4744632b652d")
                c = conn.cursor()
                command = f"SELECT version FROM version WHERE id = 1"
                print(command)
                c.execute(command)
                results = c.fetchall()
                results = str(results).replace("[('(1,", "")
                results = str(results).replace(")',)]", "")
                print(results)
                conn.commit()
                c.close()
                conn.close()
                results = float(results)+0.1
                results = "{:.1f}".format(results)
                print(f"Formated version value: {results}")
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command = f'UPDATE version SET ver={results} WHERE id=1;'
                print(command)
                c.execute(command)
                conn.commit()
                c.close()
                conn.close()
                #-------get updater channel---------
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command2 = f"select * from channels where type = 'update'"
                print(command2)
                c.execute(command2)
                results2 = c.fetchall()
                print(results2)
                conn.commit()
                c.close()
                conn.close()
                #------------------------------------
                updateEmbed = discordembed=discord.Embed(title=f"Updated to v{results}", description=f"{ctx.author.name} updated QuoteBot", color=0xf5e642)
                updateEmbed.add_field(name="Changelog:", value=f"{updated}",inline=False)
                updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
                for total in range(len(results2)):
                    sendchannel = self.bot.get_channel(results2[total][2])
                    print(sendchannel)
                    print(results2[total][2])
                    await sendchannel.send(embed=updateEmbed)

            if level=="undominor":
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
                results = str(results).replace("[('(1,", "")
                results = str(results).replace(")',)]", "")
                print(results)
                conn.commit()
                c.close()
                conn.close()
                results = float(results)-0.1
                results = "{:.1f}".format(results)
                print(f"Formated version value: {results}")
                print(results)
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command = f'UPDATE version SET ver={results} WHERE id=1;'
                print(command)
                c.execute(command)
                conn.commit()
                c.close()
                conn.close()
                #-------get updater channel---------
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command2 = f"select * from channels where type = 'update'"
                print(command2)
                c.execute(command2)
                results2 = c.fetchall()
                print(results2)
                conn.commit()
                c.close()
                conn.close()
                #------------------------------------
                updateEmbed = discordembed=discord.Embed(title=f"Undid previous minor update", description=f"{ctx.author.name} reverted QuoteBot\n\nNew version: {results}", color=0xf5e642)
                updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
                for total in range(len(results2)):
                    sendchannel = self.bot.get_channel(results2[total][2])
                    print(sendchannel)
                    print(results2[total][2])
                    await sendchannel.send(embed=updateEmbed)

            if level=="undomajor":
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
                results = str(results).replace("[('(1,", "")
                results = str(results).replace(")',)]", "")
                print(results)
                conn.commit()
                c.close()
                conn.close()
                results = float(results)-1
                print(results)
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command = f'UPDATE version SET ver={results} WHERE id=1;'
                print(command)
                c.execute(command)
                conn.commit()
                c.close()
                conn.close()
                #-------get updater channel---------
                conn = psycopg2.connect(
                host="adwess",
                database="databasename",
                user="username",
                password="password here")
                c = conn.cursor()
                command2 = f"select * from channels where type = 'update'"
                print(command2)
                c.execute(command2)
                results2 = c.fetchall()
                print(results2)
                conn.commit()
                c.close()
                conn.close()
                #------------------------------------
                updateEmbed = discordembed=discord.Embed(title=f"Undid previous major update", description=f"{ctx.author.name} reverted QuoteBot\n\nNew version: {results}", color=0xf5e642)
                updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
                for total in range(len(results2)):
                    sendchannel = self.bot.get_channel(results2[total][2])
                    print(sendchannel)
                    print(results2[total][2])
                    await sendchannel.send(embed=updateEmbed)
        else:
            await ctx.send("You are not authorised to use this command")


def setup(bot):
    bot.add_cog(Updater(bot))
