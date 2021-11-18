import discord
from discord import message
from discord.ext import commands
from  builtins import any
from discord import Intents
import requests
import os
import random
import asyncio
import psycopg2
import datetime

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setquotechannel(self, ctx):
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
        await ctx.message.delete()
        conn = connect.connectdb()
        c = conn.cursor()
        command = f"SELECT * FROM channels WHERE guild_id = {ctx.guild.id} and type='quotes'"
        print(command)
        c.execute(command)
        results = c.fetchall()
        print(results)
        if len(results) == 0:
            command = f"insert into channels(guild_id,channel_id,type) values({ctx.guild.id},{ctx.channel.id},'quotes')"
            print(command)
            c.execute(command)
            conn.commit()
            conn.close()
            await ctx.send(f"Channel <#{ctx.channel.id}> has been set as the quote channel :thumbsup:!\nCommands: **q!addquote** and **q!delquote** are now locked to this channel")
        elif len(results)==1:
            command5 = f"UPDATE channels SET channel_id={ctx.channel.id} where guild_id={ctx.guild.id} and type='quotes';" 
            print(command5)
            c.execute(command5)
            conn.commit()
            conn.close()
            await ctx.send(f"Channel <#{ctx.channel.id}> has been set as the quote channel :thumbsup:!\nCommands: **q!addquote** and **q!delquote** are now locked to this channel")
        else:
            command5 = f"delete from channels where guild_id = {ctx.guild.id} and type='quotes'" 
            print(command5)
            c.execute(command5)
            command = f"insert into channels(guild_id,channel_id,type) values({ctx.guild.id},{ctx.channel.id},'quotes')"
            print(command)
            c.execute(command)
            conn.commit()
            conn.close()
            warnmsg = await ctx.send("Your server has more then 1 channel set as type **'quotes'**! Forcing update...")
            await asyncio.selep(3)
            await ctx.send(f"Channel <#{ctx.channel.id}> has been set as the quote channel :thumbsup:!\nCommands: **q!addquote** and **q!delquote** are now locked to this channel")
            await warnmsg.delete()
    
    @setquotechannel.error
    async def channel_set_error(self, ctx, error):
        if isinstance(error, self.MissingPermissions):
            await ctx.send(f"{ctx.author.name}, You lack permission **Manage Server**")

    def get_quotes(self, uid, guild):
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        c = conn.cursor()
        command = f"SELECT * FROM quotes WHERE uid = {uid} and guild_id={guild}"
        print(command)
        c.execute(command)
        results = c.fetchall()
        conn.commit()
        conn.close()
        # print(results)
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
    async def quote(self, ctx, user: discord.User, *,partquote=None, owo=False):
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
        print("quoting...")
        print(partquote)
        print(f'is owo: {owo}')
        if partquote==None:
            userquote = self.get_rand_quote(self.get_quotes(user.id, ctx.guild.id))
            name = user.name
            if userquote is None:
                if owo==True:
                    no_quote = discord.Embed(title=f'OWNWO!!! {user} has no saved quotes on this server! uwu',description="Pwease add some with **q!addquote <user> <quote>** owo",color=0x0fff23)
                else:
                    no_quote = discord.Embed(title=f'{user} has no saved quotes on this server!',description="Add some with **q!addquote <user> <quote>**",color=0x0fff23)
                await ctx.send(embed=no_quote)
            else:
                # print('not empty! is owo?')
                # print(f'owo: {owo}')
                if owo==True:
                    # print('yes')
                    await ctx.send(f"OwO <@{user.id}>, <@{ctx.author.id}> is qowoting you UwU <3")
                embedVar = discord.Embed(title=userquote, description=" - "+str(name), color=0xB335C9)
                await ctx.send(embed=embedVar)
                print("quoted")
        else:
            # print('secondary')
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            command = f"SELECT * FROM quotes WHERE uid = {user.id} and guild_id = {ctx.guild.id} and quote LIKE '%{partquote}%'"
            print(command)
            c.execute(command)
            results = c.fetchall()
            conn.commit()
            conn.close()
            name = user.name
            if results is None:
                if owo==True:
                    no_quote = discord.Embed(title=f'OWNWO!!! {user} has no saved quotes on this server! uwu',description="Pwease add some with **q!addquote <user> <quote>** owo",color=0x0fff23)
                else:
                    no_quote = discord.Embed(title=f'{user} has no saved quotes on this server!',description="Add some with **q!addquote <user> <quote>**",color=0x0fff23)
                await ctx.send(embed=no_quote)
            elif len(results) > 1:
                # print('is loong')
                if owo==True:
                    no_quote = discord.Embed(title=f'OOPSY WOOPSY! Your query is too common!',description="This made us make a fucky wucky owo\npwetty pwease could u provide more of the quote for us uwu\nTHWANKS >.< <3\n\nA list of all your fwends qwotes can be fownd using\nq!listquotes <@fwend/fwend#0000>",color=0x0fff23)
                else:
                    no_quote = discord.Embed(title=f'Your query "{partquote}" is too common!',description="Please provide more of the quote\n\nYou can get a list of a users quote by using\nq!listquotes <@user/user#0000>",color=0x0fff23)
                await ctx.send(embed=no_quote)
            else:
                if owo==True:
                    # print('yes')
                    await ctx.send(f"OwO <@{user.id}>, <@{ctx.author.id}> is qowoting you UwU <3")
                embedVar = discord.Embed(title=results[0][2], description=" - "+str(name), color=0xB335C9)
                await ctx.send(embed=embedVar)
                print("quoted")


    @commands.command()
    async def qowote(self, ctx, user: discord.User,*,quote=None):
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
        # print(f"qowoting: {quote}")
        await self.quote(ctx, user, owo=True, partquote=quote)
        
    @commands.command()
    async def add50quotes(self, ctx):
        if ctx.author.id != 274213987514580993:
            await ctx.send("Congrats on finding a dev command!\nUnfortuntately you can't use it but still cool you found it <3")
            return
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        print("Connected to database")
        c = conn.cursor()
        print("cursored")
        for i in range(50):
            words = ["word", "bazinga", "we do be zoomin", "yup theres multiple of these fuckers!"]
            randomword = words[random.randint(0,3)]
            print(randomword)
            command = f"insert into quotes(uid,quote,date_added,guild_id) values(274213987514580993,'test{i}_{randomword}','testing_add', {ctx.guild.id});"
            print(command)
            c.execute(command)
            print("executed")
        conn.commit()
        c.close()

    @commands.command()
    async def del50quotes(self, ctx):
        print('deleting')
        print(ctx.author.id)
        if ctx.author.id != 274213987514580993:
            await ctx.send("Congrats on finding a dev command!\nUnfortuntately you can't use it but still cool you found it <3")
            return
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        print("Connected to database")
        c = conn.cursor()
        print("cursored")
        command = f"delete from quotes where uid=274213987514580993 and date_added='testing_add' and quote like 'test%';"
        print(command)
        c.execute(command)
        print("executed")
        conn.commit()
        c.close()


    @commands.command()
    async def addquote(self, ctx, user: discord.User,*, quote=""):
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
        target=user
        conn = connect.connectdb()
        c = conn.cursor()
        command = f"select * from channels where guild_id={ctx.guild.id} and type='quotes'"
        print(command)
        c.execute(command)
        print("Executed")
        results=c.fetchall()
        try:
            channel = results[0][2]
        except:
            channel = None
        print(results)
        if len(results)>1:
            print("More then one quote channel set!")
            await ctx.send("Your server has more then one quote channel set please reset your channel again using **q!setquotechannel**")
        if ctx.channel.id == channel or len(results)==0:
            if len(quote)==0:
                await ctx.send('You cannot add an empty quote! (command usage: **q!addquote <user> <quote>**)')
            else:
                print(user)
                quote2 = str(quote)
                quote = str(quote.replace("'", "''"))
                print(quote)
                command = f"select quote from quotes where quote='{quote}' AND uid='{user.id}' and guild_id={ctx.guild.id}"
                print(command)
                c.execute(command)
                print("Executed")
                results=c.fetchall()
                print(results)
                print(len(results))
                if len(results)==0:
                    embedVar4 = discord.Embed(title="Confirm Quote",description="Please confirm that this is the quote you wish to add", color=0x00ff2f)
                    embedVar4.add_field(name=f'  "{quote2}"', value=f"    -{target.name}\n\nPlease react with ✅ to confirm or ❎ to cancel", inline=False)
                    message = await ctx.send(embed=embedVar4)
                    await message.add_reaction('✅')
                    await message.add_reaction('❎')

                    def check(reaction, user):
                        return user == ctx.author# and str(reaction.emoji) == '✅'

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                        await message.clear_reactions()
                    except asyncio.TimeoutError:
                        await message.clear_reactions()

                    if str(reaction.emoji)=='✅':
                        print("Reacted with YES")
                        command = f"insert into quotes(uid,quote,date_added,guild_id) values({target.id},'{quote}','{datetime.datetime.now().strftime('%d/%m/%Y')}',{ctx.guild.id});"
                        print(command)
                        c.execute(command)
                        print("executed")
                        conn.commit()
                        c.close()
                        conn.close()
                        donemessage = discord.Embed(title="Quote Added!", color=0x00ff2f)
                        donemessage.timestamp = datetime.datetime.utcnow()
                        donemessage.add_field(name=f"\"{quote}\"", value=f"-{target.name}")
                        donemessage.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                        await ctx.message.delete()
                        await message.clear_reactions()
                        await message.edit(embed=donemessage)
                        log = self.bot.get_cog("Logger")
                        await log.logger(command=f'**Added a quote** to {target}: "{quote}"', user=ctx.author, channel=ctx.channel, color="#55ff21", guild=ctx.message.guild.id)
                        print("done and logged")
                    elif str(reaction.emoji)=='❎':
                        await ctx.message.delete()
                        await message.clear_reactions()
                        cancelmsg = discord.Embed(title="Canceled", color=0xeb0c0c)
                        await message.edit(embed=cancelmsg)
                        await asyncio.sleep(4)
                        await message.delete()
                
                else:
                    await ctx.send("Sorry the quote you are trying to add already exists for that user")
        else:
            await ctx.send(f"Commands **q!addquote** and **q!delquote** are locked to channel <#{results[0][2]}>")

    @commands.command()
    async def delquote(self, ctx, user: discord.User,*, quote=""):
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
        target=user
        conn = connect.connectdb()
        c = conn.cursor()
        command = f"select * from channels where guild_id={ctx.guild.id} and type='quotes'"
        print(command)
        c.execute(command)
        print("Executed")
        results=c.fetchall()
        print(results)
        if len(results) == 0:
            channel = None
        else:
            channel = results[0][2]
        if len(results)>1:
            print("More then one quote channel set!")
            await ctx.send("Your server has more then one quote channel set please reset your channel again using **q!setquotechannel**")
        if channel == ctx.channel.id or channel==None:
            print('channels')
            if len(quote)==0:
                await ctx.send("Please enter a part of the quote you wish to remove (command usage: **q!delquote <user> <part-of-quote>**)")
                return
            target=user
            command = f"select * from quotes where quote like '%{quote}%' AND uid='{user.id}' and guild_id={ctx.guild.id}"
            print(command)
            c.execute(command)
            result = c.fetchall()
            print(result)
            print(len(result))
            if (len(result) == 3 or len(result)==2):
                print("len is == 3 or 2")
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
                    return user == ctx.author# and str(reaction.emoji) == '✅'

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                        print('emoji clicked')
                        print(reaction.emoji)
                        await message.remove_reaction(reaction, user)
                    except asyncio.TimeoutError:
                        await message.clear_reactions()

                    if str(reaction.emoji) == '1️⃣':
                        await ctx.message.delete()
                        await message.clear_reactions()
                        result = str(result[0][2]).replace("'", "''")
                        command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id} and guild_id={ctx.guild.id}"
                        print(command)
                        c.execute(command)
                        print("executed")
                        donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                        print("set donemessage")
                        await message.edit(embed=donemessage)
                        print("edited")
                        await asyncio.sleep(4)
                        await message.delete()
                        print("deleted")
                        log = self.bot.get_cog("Logger")
                        await log.logger(command=f"**Deleted quote** from {target}: \"{result}\"", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                        print("Deleted")
                    if str(reaction.emoji) == '2️⃣':
                        await ctx.message.delete()
                        await message.clear_reactions()
                        c = conn.cursor()
                        result = str(result[1][2]).replace("'", "''")
                        command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id};"
                        print(command)
                        c.execute(command)
                        donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                        await message.edit(embed=donemessage)
                        await asyncio.sleep(4)
                        await message.delete()
                        log = self.bot.get_cog("Logger")
                        await log.logger(command=f"**Deleted quote** from {target}: \"{result}\"", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                        print("Deleted")
                    if str(reaction.emoji) == '3️⃣':
                        await ctx.message.delete()
                        await message.clear_reactions()
                        c = conn.cursor()
                        result = str(result[2][2]).replace("'", "''")
                        command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id};"
                        print(command)
                        c.execute(command)
                        donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                        await message.edit(embed=donemessage)
                        await asyncio.sleep(4)
                        await message.delete()
                        log = self.bot.get_cog("Logger")
                        await log.logger(command=f"**Deleted quote** from {target}: \"{result}\"", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                        print("Deleted")

                    elif str(reaction.emoji) == '❎':
                        await ctx.message.delete()
                        await message.clear_reactions()
                        cancelmsg = discord.Embed(title="Canceled", color=0xeb0c0c)
                        await message.edit(embed=cancelmsg)
                        await asyncio.sleep(4)
                        await message.delete()
                    conn.commit()
                    c.close()
                    conn.close()

            elif (len(result)==1):
                embedVar4 = discord.Embed(title="Confirm Quote",description="Please confirm that this is the quote you wish to remove", color=0xff0a0a)
                embedVar4.add_field(name=f'   "{result[0][2]}"', value=f"     -{user.name}\n\nPlease react with ✅ to confirm or ❎ to cancel", inline=False)
                message = await ctx.send(embed=embedVar4)
                await message.add_reaction('✅')
                await message.add_reaction('❎')


                def check(reaction, user):
                    return user == ctx.author# and str(reaction.emoji) == '✅'

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                        await message.remove_reaction(reaction, user)
                    except asyncio.TimeoutError:
                        await message.clear_reactions()

                    if str(reaction.emoji) == '✅':
                        await ctx.message.delete()
                        await message.clear_reactions()
                        result = str(result[0][2].replace("'", "''"))
                        command = f"DELETE FROM quotes WHERE quote = '{result}' AND uid = {target.id};"
                        print(command)
                        c.execute(command)
                        donemessage = discord.Embed(title="Quote Removed", color=0xeb0c0c)
                        await message.edit(embed=donemessage)
                        await asyncio.sleep(4)
                        await message.delete()
                        log = self.bot.get_cog("Logger")
                        await log.logger(command=f"**Deleted quote** from {target}: \"{result}\"", user=ctx.author, channel=ctx.channel, color="#f54242", guild=ctx.message.guild.id)
                        print("Deleted")

                    elif str(reaction.emoji) == '❎':
                        await ctx.message.delete()
                        await message.clear_reactions()
                        cancelmsg = discord.Embed(title="Canceled", color=0xeb0c0c)
                        await message.edit(embed=cancelmsg)
                        await asyncio.sleep(4)
                        await message.delete()
                    conn.commit()
                    c.close()
                    conn.close()
            

            elif len(result)>3: 
                no_quote = discord.Embed(title=f'The query "{quote}" is too common!',description="Please provide more of the quote",color=0x0fff23)
                await ctx.send(embed=no_quote)

            elif len(result)==0: 
                no_quote = discord.Embed(title=f'No quote "{quote}" found!',color=0x0fff23)
                await ctx.send(embed=no_quote)
        else:
            await ctx.send(f"Commands **q!addquote** and **q!delquote** are locked to channel <#{results[0][2]}>")

        # conn.commit()
        # c.close()
        # conn.close()

    @commands.command()
    async def listquotes(self, ctx, user: discord.User, *, page=1):
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
        conn = connect.connectdb()
        c = conn.cursor()
        command = f"SELECT * FROM quotes WHERE uid = {user.id} and guild_id = {ctx.guild.id}"
        print(command)
        c.execute(command)
        print("executed")
        results = c.fetchall()
        # print(results)
        conn.commit()
        conn.close()
        print(len(results))
        n_results = []
        for quotes in results:
            try:
                n_results.append(quotes[2])
            except:
                pass
        # print(type(results))
        if len(results)>10:
            print("greater then 25")
            pages = []
            split_quotes = [n_results[x:x+10] for x in range(0, len(n_results),10)]
            print("Split to page count")
            # print(split_quotes)
            print(len(split_quotes))
            i=0
            pagenum=1
            for pagess in split_quotes:
                # print(pagess)
                page = discord.Embed (
                    title = f'Quotes for {user.name} (Page {pagenum}/{len(split_quotes)})',
                    description = f'*from server: {ctx.guild.name}*',
                    colour = 0x00ff00
                )
                page.timestamp = datetime.datetime.utcnow()
                page.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                for quotes in split_quotes[i]:
                    # print(quotes)
                    page.add_field(name=f"{quotes}", value=f"-{user.name}")
                pages.append(page)
                i=i+1
                pagenum=pagenum+1

            print(pages)

            message = await ctx.send(embed = pages[0])

            await message.add_reaction('▶')

            def check(reaction, user):
                return user == ctx.author
            timeouts=False
            i = 0
            while timeouts==False:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
                    await message.clear_reactions()
                except asyncio.TimeoutError:
                    timeouts=True
                    await message.clear_reactions()
                    break
                
                if str(reaction.emoji) == '◀':
                    i -= 1
                    # print(i)
                    if i == 0:
                        await message.edit(embed = pages[i])
                        await message.add_reaction('▶')

                    elif i>0 and i<len(split_quotes)-1:
                        await message.edit(embed = pages[i])
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')

                elif str(reaction.emoji) == '▶':
                    i+=1
                    # print(i)
                    if i == len(split_quotes)-1:
                        await message.edit(embed = pages[i])
                        await message.add_reaction('◀')
                        
                    elif i>0 and i != len(split_quotes)-1:
                        await message.edit(embed = pages[i])
                        await message.add_reaction('◀')
                        await message.add_reaction('▶')

            
        elif len(results)<=10 and len(results)>0:
            page1 = discord.Embed (
                title = f'Quotes for {user.name} (Page 1/1)',
                description = f'*from server: {ctx.guild.name}*',
                colour = 0x00ff00
            )
            page1.timestamp = datetime.datetime.utcnow()
            page1.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                
            for i in range(len(n_results)):
                page1.add_field(name=f"{n_results[i]}", value=f"-{user.name}")
            pages = [page1]
            message = await ctx.send(embed = page1)
        else:
            no_quote = discord.Embed(title='This user has no saved quotes on this server!',color=0x0fff23)
            no_quote.timestamp = datetime.datetime.utcnow()
            no_quote.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                
            await ctx.send(embed=no_quote)

    @quote.error
    async def arg_error_quote(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send('Incorrect arguments entered | usage: **q!quote <@user/user#0000> <part-of-quote>**')

    @qowote.error
    async def arg_error_qowote(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send('Incorrect arguments entered | usage: **q!qowote <@user/user#0000> <part-of-quote>**')

    @addquote.error
    async def arg_error_addquote(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send('Incorrect arguments entered | usage: **q!addquote <@user/user#0000> <quote>**')

    @delquote.error
    async def arg_error_delquote(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send('Incorrect arguments entered | usage: **q!delquote <@user/user#0000> <part-of-quote>**')
        

    @listquotes.error
    async def arg_error_listquotes(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            await ctx.send('Incorrect arguments entered | usage: **q!listquotes <@user/user#0000>**')




def setup(bot):
    bot.add_cog(Quotes(bot))