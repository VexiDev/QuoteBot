import discord
from discord.ext import commands, tasks
from  builtins import any
from discord import Intents
import requests
import os
import random
import asyncio
import datetime
import psycopg2
import topgg
import traceback

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @tasks.loop(hours=12)
    async def update_stats(self):
        try:
            await self.bot.topggpy.post_guild_count()
            print(f"Posted server count ({self.bot.topggpy.guild_count})")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")


    async def checkblist(self, ctx, user):
        # print('going')
        conn = self.connectdb()
        # print("Connected to database")
        c = conn.cursor()
        command = f"select * from users where uid={user.id}"
        # print(command)
        c.execute(command)
        # print("executed")
        results = c.fetchall()
        # print(results)
        conn.commit()
        c.close()
        if results[0][3]==True:
            blacklist = discord.Embed(title=f"<:no:907768020561190983> Blacklisted", description=f"The account **{user}** with ID **{user.id}** is globally blacklisted\n**Reason:** {results[0][7]}\n*Blacklists cannot be appealed*", color=0xff0000)
            blacklist.timestamp = datetime.datetime.utcnow()
            blacklist.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            return(blacklist, "global")
        elif results[0][4]==True:
            blacklist = discord.Embed(title=f"<:no:907768020561190983> Blacklisted", description=f"The account **{user}** with ID **{user.id}** is support blacklisted\n**Reason:** {results[0][7]}\n*Blacklists cannot be appealed*", color=0xff0000)
            blacklist.timestamp = datetime.datetime.utcnow()
            blacklist.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            return(blacklist, "support")
        else:
            return None

    @commands.command()
    async def blist(self, ctx, command, user: discord.User, type, *,reason="None"):
        if ctx.author.id != 274213987514580993:
            return
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        print("Connected to database")
        c = conn.cursor()
        sqlcommand = f"select * from users where uid={user.id}"
        print(sqlcommand)
        c.execute(sqlcommand)
        print("executed")
        results = c.fetchall()
        print(results)
        conn.commit()
        c.close()
        if command.lower()=="add":
            if type.lower()=="global":
                if results[0][3]==True:
                    deny = discord.Embed(title=f"<:redTick:892436376673464340> User {user} is already globally blacklisted", color=0xff0000)
                    await ctx.send(embed=deny)
                else:
                    connect = self.bot.get_cog("Misc")
                    conn = connect.connectdb()
                    print("Connected to database")
                    c = conn.cursor()
                    sqlcommand = f"update users set global_blist=True where uid={user.id}"
                    print(sqlcommand)
                    c.execute(sqlcommand)
                    print("executed")
                    sqlcommand = f"update users set blist_reason='{reason}' where uid={user.id}"
                    print(sqlcommand)
                    c.execute(sqlcommand)
                    print("executed")
                    conn.commit()
                    c.close()
                    accept = discord.Embed(title=f"<:rbcheck:892331857440559124> User {user} added to globally blacklist", color=0xff0000)
                    await ctx.send(embed=accept)
            elif type.lower()=="support":
                if results[0][4]==True:
                    deny=discord.Embed(title=f"<:redTick:892436376673464340> User {user} is already support blacklisted", color=0xff0000)
                    await ctx.send(embed=deny)
                else:
                    connect = self.bot.get_cog("Misc")
                    conn = connect.connectdb()
                    print("Connected to database")
                    c = conn.cursor()
                    sqlcommand = f"update users set support_blist=True where uid={user.id}"
                    print(sqlcommand)
                    c.execute(sqlcommand)
                    print("executed")
                    sqlcommand = f"update users set blist_reason='{reason}' where uid={user.id}"
                    print(sqlcommand)
                    c.execute(sqlcommand)
                    print("executed")
                    conn.commit()
                    c.close()
                    accept = discord.Embed(title=f"<:rbcheck:892331857440559124> User {user} added to support blacklist", color=0xff0000)
                    await ctx.send(embed=accept)
            else:
                pass
        elif command.lower()=="remove":
            if type.lower()=="global":
                if results[0][3]==False:
                    deny = discord.Embed(title=f"<:redTick:892436376673464340> User {user} is not globally blacklisted", color=0xff0000)
                    await ctx.send(embed=deny)
                else:
                    connect = self.bot.get_cog("Misc")
                    conn = connect.connectdb()
                    print("Connected to database")
                    c = conn.cursor()
                    sqlcommand = f"update users set global_blist=False where uid={user.id}"
                    print(sqlcommand)
                    c.execute(sqlcommand)
                    print("executed")
                    conn.commit()
                    c.close()
                    accept = discord.Embed(title=f"<:rbcheck:892331857440559124> User {user} removed from global blacklist", color=0xff0000)
                    await ctx.send(embed=accept)

            elif type.lower()=="support":
                if results[0][4]==False:
                    deny=discord.Embed(title=f"<:redTick:892436376673464340> User {user} is not support blacklisted", color=0xff0000)
                    await ctx.send(embed=deny)
                else:
                    connect = self.bot.get_cog("Misc")
                    conn = connect.connectdb()
                    print("Connected to database")
                    c = conn.cursor()
                    sqlcommand = f"update users set support_blist=False where uid={user.id}"
                    print(sqlcommand)
                    c.execute(sqlcommand)
                    print("executed")
                    conn.commit()
                    c.close()
                    accept = discord.Embed(title=f"<:rbcheck:892331857440559124> User {user} removed from support blacklist", color=0xff0000)
                    await ctx.send(embed=accept)
                    
            else:
                await ctx.send(f"Invalid Type '{type}'. Types: global/support")
        else:
            await ctx.send(f"Invalid Action '{command}'. Actions: add/remove")

    @commands.command()
    async def test(self, ctx):
        await ctx.send("tested")

    def connectdb(self):
        conn = psycopg2.connect(        
        host="ec2-52-72-60-116.compute-1.amazonaws.com",
        database="datps9doutonos",
        user="u892s7k90calmu",
        password="p772707b18a9153e9df8335e17840905533f470e050aa31ef0d855b193e762080") 
        return(conn)

    @commands.command()
    async def topserver(self, ctx):
        if ctx.author.id != 274213987514580993:
            return
        msg=""
        for guilds in self.bot.guilds:
            msg = msg+f"{guilds.name} - {len(guilds.members)}\n"
        await ctx.send(msg)
        
    @commands.command()
    async def removebots(self, ctx):
        if ctx.author.id != 274213987514580993:
            return   
        try:
            msg = await ctx.send("Removing bots")
            conn = self.connectdb()
            c = conn.cursor()
            command = f"SELECT uid FROM users"
            c.execute(command)
            userlist = c.fetchall()
            totalbots=0
            await msg.edit(f"Total users: {len(userlist)}\nRemoved: {totalbots}")
            # print(userlist)
            for uid in userlist:
                # print(uid[0])
                user = discord.utils.get(self.bot.get_all_members(), id=uid[0])
                # print(user.name)
                break
                if user == None:
                    # print("is none")
                    pass
                elif user.bot != True:
                    # print("not a bot")
                    pass
                else:
                    print(f"Bot Removed: {user.name} | {user.id}")
                    command = f"delete from users where uid={uid[0]}"
                    c.execute(command)
                    conn.commit()
                    totalbots=totalbots+1
                    if (totalbots%5) == 0:
                        await msg.edit(f"Total users: {len(userlist)}\nRemoved: {totalbots}")
            c.close()
            await msg.edit(f"Removed {totalbots} from user table")
        except:
            traceback.print_exc()

    @commands.command()
    async def invite(self,ctx):
            await ctx.send("https://discord.com/oauth2/authorize?client_id=814379239930331157&permissions=93264&scope=bot")
    

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.channels:
            print(channel.name)
            try:
                msg = await channel.send("Thanks for inviting Quotebot! I am currently setting up your server for use. This may take a couple minutes.\n\nStatus: <a:loading:892534287415525386> Setting everything up")
                break
            except:
                traceback.print_exc
                pass
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        print("Connected to database")
        c = conn.cursor()
        # print("cursored")
        try:
                print(f'Checking for guild: {guild.name}\n------------')
                for user in guild.members:
                    date=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    print(date)
                    print(f'checking user: {user}')
                    command = f"select * from users where uid={user.id}"
                    # print(command)
                    c.execute(command)
                    # print("executed")
                    result = c.fetchall()
                    if len(result)==0 and user.bot==False:
                        command = f"insert into users(uid, nsfw, global_blist, support_blist,support_cooldown, support_time) values({user.id}, False, False, False, False, '{date}')"
                        # print(command)
                        c.execute(command)
                        # print("executed")
                        print('added user\n----------')
                    else:
                        print("duplicate user or bot\n----------")
                    await asyncio.sleep(0.2)
        except:
            trace.print_exc()
        conn.commit()
        c.close()
        await msg.edit("Your server is ready to use quotebot! Get a list of commands using **q!help**")

    @commands.command()
    async def info(self, ctx):
        # connect = self.bot.get_cog("Misc")
        # print('gotten connect')
        try:
            blist = await self.checkblist(ctx, ctx.author)
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
        infoEmbed = discord.Embed(title=f"QuoteBot Info", description=f"\nCurrent version: **{final_ver_results}**\nTotal quotes logged: **{str(results_total_quotes[0]).replace('(', '').replace(',)','')}**\nTotal unique users: **{str(results_total_users[0]).replace('(', '').replace(',)','')}**\nTotal servers: **{guilds}**", color=0xf5e642)
        await ctx.send(embed=infoEmbed)

def setup(bot):
    bot.add_cog(Misc(bot))