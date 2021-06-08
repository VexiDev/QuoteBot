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
import sys

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_quotes(self, uid):
        conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password")
        c = conn.cursor()
        command = f"SELECT * FROM quotes WHERE uid = {uid}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        conn.commit()
        conn.close()
        print(results)
        return results

    def get_rand_quote(self, userquotes):
        if len(userquotes) != 0:
            print(len(userquotes))
            randnum = random.randint(0, len(userquotes)-1)
            randquote = userquotes[randnum][2]
            return(randquote)
        else:
            return(None)

    @commands.command()
    async def quote(self, ctx, user: discord.Member=None):
        print("quoting...")
        userquote = self.get_rand_quote(self.get_quotes(user.id))
        name = user.name
        if userquote is None:
            await ctx.send(f"**No quote found for {name}**")
        else:
            embedVar = discord.Embed(title=userquote, description=" - "+str(name), color=0xB335C9)
            await ctx.send(embed=embedVar)
            print("quoted")
            log = self.bot.get_cog('Logger') 
            print("log var set")
            print(log)
            await log.logger(command=f"**Quoted** {user}", user=ctx.author, channel=ctx.channel, color="#55ff21", guild=ctx.guild.id)
            # await log.logger("QUOTE UWU", ctx.author)
            print("ran logger line")

    @commands.command()
    async def qowote(self, ctx, user: discord.User):
        await ctx.send(f"OwO <@{user.id}>, <@{ctx.author.id}> is qowoting you UwU <3")
        await self.quote(ctx, user)
        
    @commands.command()
    async def addquote(self, ctx, user: discord.User,*, quote=""):
        author = ctx.message.author
        conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password")
        c = conn.cursor()
        command = f"SELECT * FROM permission WHERE uid = {author.id} and guild_id = {ctx.guild.id}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        print(results)
        conn.commit()
        c.close()
        conn.close()
        print(results)
        permcount = 0
        for perm in results:
            if(perm[2] == 'addquote'):
                print(user)
                target=user
                quote2 = str(quote)
                quote = str(quote.replace("'", "''"))
                print(quote)
                conn = psycopg2.connect(
                host="host",
                database="database",
                user="user",
                password="password")
                c = conn.cursor()
                command = f"select quote from quotes where quote='{quote}' AND uid='{user.id}'"
                print(command)
                c.execute(command)
                print("Executed")
                results=c.fetchall()
                print(results)
                conn.commit()
                c.close()
                conn.close()
                print(len(results))
                if len(results)==0:
                    embedVar4 = discord.Embed(title="Confirm Quote",description="Please confirm that this is the quote you wish to add", color=0x00ff2f)
                    embedVar4.add_field(name=f'  "{quote2}"', value=f"    -{target.name}\n\nPlease react with ✅ to confirm or ❎ to cancel", inline=False)
                    message = await ctx.send(embed=embedVar4)
                    await message.add_reaction('✅')
                    await message.add_reaction('❎')

                    def check(reaction, user):
                        return user == ctx.author
                    reaction = None

                    while True:
                        if str(reaction) == '✅':
                            print("Reacted with YES")
                            conn = psycopg2.connect(
                            host="host",
                            database="database",
                            user="user",
                            password="password")
                            print("Connected to database")
                            c = conn.cursor()
                            print("cursored")
                            command = f"insert into quotes(uid,quote) values({target.id},'{quote}');"
                            print(command)
                            c.execute(command)
                            print("executed")
                            conn.commit()
                            c.close()
                            conn.close()
                            donemessage = discord.Embed(title="Quote Added", color=0x00ff2f)
                            await ctx.message.delete()
                            await message.clear_reactions()
                            await message.edit(embed=donemessage)
                            await asyncio.sleep(4)
                            await message.delete()
                            log = self.bot.get_cog("Logger")
                            await log.logger(command=f'**Added a quote** to {target}: "{quote}"', user=ctx.author, channel=ctx.channel, color="#55ff21", guild=ctx.message.guild.id)
                            print("done and logged")

                        elif str(reaction) == '❎':
                            await ctx.message.delete()
                            await message.clear_reactions()
                            cancelmsg = discord.Embed(title="Canceled", color=0xeb0c0c)
                            await message.edit(embed=cancelmsg)
                            await asyncio.sleep(4)
                            await message.delete()
                    
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
                            await message.remove_reaction(reaction, user)
                        except:
                            break
                else:
                    await ctx.send("Sorry the quote you are trying to add already exists for that user")
            else: 
                permcount = permcount+1
                
        if permcount == len(results):
            await ctx.send("You lack permission to use this command.")
            log = self.bot.get_cog("Logger")
            await log.logger(command=f"Tried to add a quote {quote} to {target} but lacks permission", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)


    @commands.command()
    async def delquote(self, ctx, user: discord.User,*, quote=""):
        target=user
        author = ctx.message.author
        conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password")
        c = conn.cursor()
        command = f"SELECT * FROM permission WHERE uid = {author.id} and guild_id = {ctx.guild.id}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        print(results)
        conn.commit()
        c.close()
        conn.close()
        print(results)
        permcount = 0
        for perm in results:
            if(perm[2] == 'delquote'):
                conn = psycopg2.connect(
                host="host",
                database="database",
                user="user",
                password="password")
                c = conn.cursor()
                command = f"select * from quotes where quote like '%{quote}%' AND uid='{user.id}'"
                print(command)
                c.execute(command)
                result = c.fetchall()
                print(result)
                print(len(result))
                conn.commit()
                c.close()
                conn.close()
                if (len(result) == 3 or len(result)==2):
                    print("len is -=3 or 2")
                    # for i in range(len(result)):
                    #     result = result.replace("('", "")
                    #     result = result.replace("',)", "")
                    #     result = result.replace('("', "")
                    #     result = result.replace('",)', '')
                    #     result = result.replace('[', "")
                    #     result = result.replace(']', '')
                    # print(result)

                    embedVar4 = discord.Embed(title="Confirm Quote",description="Please confirm that this is the quote you wish to remove", color=0xff0a0a)
                    print("made embedvar4")
                    for i in range(len(result)):
                        quotee=result[i][2]
                        print(quotee)
                        embedVar4.add_field(name=f'   "{quotee}"', value=f"     -{user.name}", inline=False)
                        print("added 1 field")
                # embedVar4.add_field(name="Please react with 1️⃣ , 2️⃣ , 3️⃣ to select which quote you would like to delete or react with ❎ to cancel", inline=False)
                    print("added fields")
                    message = await ctx.send(embed=embedVar4)
                    print("sent")
                    print(f"length of result is {len(result)}")
                    if( len(result)==2):
                        print("length is 2")
                        await message.add_reaction('1️⃣')
                        print("added 1")
                        await message.add_reaction('2️⃣')
                        print("added 2")
                        await message.add_reaction('❎')
                        print("added X")

                    elif (len(result)==3):
                        print("length is 3")
                        await message.add_reaction('1️⃣')
                        print("added 1")
                        await message.add_reaction('2️⃣')
                        print("added 2")
                        await message.add_reaction('3️⃣')
                        print("added 3")
                        await message.add_reaction('❎')
                        print("added X")

                    def check(reaction, user):
                        return user == ctx.author
                    reaction = None
                
                    while True:
                        if str(reaction) == '1️⃣':
                            await ctx.message.delete()
                            await message.clear_reactions()
                            conn = psycopg2.connect(
                            host="host",
                            database="database",
                            user="user",
                            password="password")
                            c = conn.cursor()
                            result = str(result[0][2]).replace("'", "''")
                            command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id};"
                            print(command)
                            c.execute(command)
                            print("executed")
                            conn.commit()
                            c.close()
                            conn.close()
                            donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                            print("set donemessage")
                            await message.edit(embed=donemessage)
                            print("edited")
                            await asyncio.sleep(4)
                            await message.delete()
                            print("deleted")
                            log = self.bot.get_cog("Logger")
                            await log.logger(command=f"**Deleted quote** from {user} '{result}'", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                            print("Deleted")
                        if str(reaction) == '2️⃣':
                            await ctx.message.delete()
                            await message.clear_reactions()
                            conn = psycopg2.connect(
                            host="host",
                            database="database",
                            user="user",
                            password="password")
                            c = conn.cursor()
                            result = str(result[1][2]).replace("'", "''")
                            command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id};"
                            print(command)
                            c.execute(command)
                            conn.commit()
                            c.close()
                            conn.close()
                            donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                            await message.edit(embed=donemessage)
                            await asyncio.sleep(4)
                            await message.delete()
                            log = self.bot.get_cog("Logger")
                            await log.logger(command=f"**Deleted quote** from {user} '{result}'", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                            print("Deleted")
                        if str(reaction) == '3️⃣':
                            await ctx.message.delete()
                            await message.clear_reactions()
                            conn = psycopg2.connect(
                            host="host",
                            database="database",
                            user="user",
                            password="password")
                            c = conn.cursor()
                            result = str(result[2][2]).replace("'", "''")
                            command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id};"
                            print(command)
                            c.execute(command)
                            conn.commit()
                            c.close()
                            conn.close()
                            donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                            await message.edit(embed=donemessage)
                            await asyncio.sleep(4)
                            await message.delete()
                            log = self.bot.get_cog("Logger")
                            await log.logger(command=f"**Deleted quote** from {user} '{result}'", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                            print("Deleted")

                        elif str(reaction) == '❎':
                            await ctx.message.delete()
                            await message.clear_reactions()
                            cancelmsg = discord.Embed(title="Canceled", color=0xeb0c0c)
                            await message.edit(embed=cancelmsg)
                            await asyncio.sleep(4)
                            await message.delete()
                
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
                            await message.remove_reaction(reaction, user)
                        except:
                            break

                elif (len(result)==1):
                    embedVar4 = discord.Embed(title="Confirm Quote",description="Please confirm that this is the quote you wish to remove", color=0xff0a0a)
                    embedVar4.add_field(name=f'   "{result[0][2]}"', value=f"     -{user.name}\n\nPlease react with ✅ to confirm or ❎ to cancel", inline=False)
                    message = await ctx.send(embed=embedVar4)
                    await message.add_reaction('✅')
                    await message.add_reaction('❎')

                    def check(reaction, user): 
                        return user == ctx.author
                    reaction = None
                
                    while True:
                        if str(reaction) == '✅':
                            await ctx.message.delete()
                            await message.clear_reactions()
                            conn = psycopg2.connect(
                            host="host",
                            database="database",
                            user="user",
                            password="password")
                            c = conn.cursor()
                            result = str(result[0][2].replace("'", "''"))
                            command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id};"
                            print(command)
                            c.execute(command)
                            conn.commit()
                            c.close()
                            conn.close()
                            donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                            await message.edit(embed=donemessage)
                            await asyncio.sleep(4)
                            await message.delete()
                            log = self.bot.get_cog("Logger")
                            await log.logger(command=f"**Deleted quote** from {user} '{result}'", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                            print("Deleted")

                        elif str(reaction) == '❎':
                            await ctx.message.delete()
                            await message.clear_reactions()
                            cancelmsg = discord.Embed(title="Canceled", color=0xeb0c0c)
                            await message.edit(embed=cancelmsg)
                            await asyncio.sleep(4)
                            await message.delete()
                
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout = 30.0, check = check)
                            await message.remove_reaction(reaction, user)
                        except:
                            break
                else: 
                    await ctx.send("No quote found or filter term to common (q$listquotes)")
            else:
                permcount = permcount+1
                print(permcount)
        print(permcount)
        print(len(results))
        if permcount == len(results):
            await ctx.send("You lack permission to use this command.")
            log = self.bot.get_cog("Logger")
            print("set log")
            await log.logger(command=f"Tried to delete a quote from {target} but lacks permission\ninput: *'{quote}'*", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
            print("logged")

    @commands.command()
    async def listquotes(self, ctx, user: discord.User, *, page=1):
        conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password")
        c = conn.cursor()
        command = f"SELECT quote FROM quotes WHERE uid = {user.id}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        conn.commit()
        conn.close()
        for i in range(len(results)): 
            results[i] = str(results[i]).replace("('", "")
            results[i] = str(results[i]).replace("',)", "")
            results[i] = str(results[i]).replace('("', "")
            results[i] = str(results[i]).replace('",)', '')
        embedVar7 = discord.Embed(title=f"Quotes for {user.name} (Page {page})", description="A list of all logged quotes for a user", color=0x00ff00)
        print(len(results))
        print(results)
        if len(results)>25:
            page1 = discord.Embed (
                title = f'Quotes for {user.name} (Page 1/2)',
                description = 'A list of all logged quotes for a user',
                colour = 0x00ff00
            )
            loopvar = 0
            while loopvar < 24:
                page1.add_field(name=f"{results[loopvar]}", value=f"-{user.name}")
                loopvar = loopvar+1
            page2 = discord.Embed (
                title = f'Quotes for {user.name} (Page 2/2)',
                description = 'A list of all logged quotes for a user',
                colour = 0x00ff00   
            )
            loopvar = 25
            while loopvar < len(results):
                page2.add_field(name=f"{results[loopvar]}", value=f"-{user.name}")
                loopvar = loopvar+1
            # page3 = discord.Embed (
            #     title = f'Quotes for {user.name} (Page 3/4)',
            #     description = 'A list of all logged quotes for a user',
            #     colour = 0x00ff00   
            # )
            # loopvar = 25
            # while loopvar < len(results):
            #     page2.add_field(name=f"{results[loopvar]}", value=f"-{user.name}")
            #     loopvar = loopvar+1
            # page4 = discord.Embed (
            #     title = f'Quotes for {user.name} (Page 4/4)',
            #     description = 'A list of all logged quotes for a user',
            #     colour = 0x00ff00   
            # )
            # loopvar = 25
            # while loopvar < len(results):
            #     page2.add_field(name=f"{results[loopvar]}", value=f"-{user.name}")
            #     loopvar = loopvar+1
            pages = [page1, page2]

            message = await ctx.send(embed = page1)

            await message.add_reaction('◀')
            await message.add_reaction('▶')

            def check(reaction, user):
                return user == ctx.author

            i = 0
            reaction = None

            while True:
                if str(reaction) == '◀':
                    if i > 0:
                        i -= 1
                        await message.edit(embed = pages[i])
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')
                elif str(reaction) == '▶':
                    if i < 2:
                        i += 1
                        await message.edit(embed = pages[i])
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')
                elif str(reaction) == '▶':
                    if i == 1:
                        i == 1
                        await message.edit(embed = pages[i])
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')
                elif str(reaction) == '◀':
                    if i == 0:
                        i == 0
                        await message.edit(embed = pages[i])
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')
                # elif str(reaction) == '▶':
                #     if i == 2:
                #         i == 3
                #         await message.edit(embed = pages[i])
                #         await message.add_reaction('◀')
                #         await message.add_reaction('▶')
                # elif str(reaction) == '◀':
                #     if i == 3:
                #         i == 2
                #         await message.edit(embed = pages[i])
                #         await message.add_reaction('◀')
                #         await message.add_reaction('▶')
                # elif str(reaction) == '▶':
                #     if i == 3:
                #         i == 4
                #         await message.edit(embed = pages[i])
                #         await message.add_reaction('◀')
                #         await message.add_reaction('▶')
                # elif str(reaction) == '◀':
                #     if i == 4:
                #         i == 3
                #         await message.edit(embed = pages[i])
                #         await message.add_reaction('◀')
                #         await message.add_reaction('▶')
                
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout = 120.0, check = check)
                    await message.remove_reaction(reaction, user)
                except:
                    break
                await message.clear_reactions()
            
        else:
            page1 = discord.Embed (
                title = f'Quotes for {user.name} (Page 1/1)',
                description = 'A list of all logged quotes for a user',
                colour = 0x00ff00
            )
            for i in range(len(results)):
                page1.add_field(name=f"{results[i]}", value=f"-{user.name}")
            pages = [page1]
            message = await ctx.send(embed = page1)

def setup(bot):
    bot.add_cog(Quotes(bot))