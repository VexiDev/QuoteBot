import discord
from discord import *
from discord.ext import commands
from  builtins import any
from discord import Intents
import requests
import os
import random
import asyncio
import psycopg2
from collections import Counter
import traceback as trace
from discord_components import *
import datetime

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setbio(self, ctx,*, bio=""):
        if ctx.author.bot == True:
            return
        try:
            connect = self.bot.get_cog("Misc")

            try:
                blist = await connect.checkblist(ctx, ctx.author)
            except:
                trace.print_exc()

            if blist is not None:
                if blist[1]=="global":

                    await ctx.send(embed=blist[0])
                    return
                else:
                    pass
            else:
                pass

            conn = connect.connectdb()
            c = conn.cursor()
            command = f"update users set bio='{bio}' where uid={ctx.author.id}"
            print(command)
            c.execute(command)
            print('executed')
            conn.commit()
            conn.close()
            await ctx.send('succesfully updated your bio')
        except:
            trace.print_exc()

    @commands.command()
    async def star(self, ctx,*,quote):        
        if ctx.author.bot == True:
            return
        try:
            connect = self.bot.get_cog("Misc")

            try:
                blist = await connect.checkblist(ctx, ctx.author)
            except:
                trace.print_exc()

            if blist is not None:
                if blist[1]=="global":

                    await ctx.send(embed=blist[0])
                    return
                else:
                    pass
            else:
                pass

            conn = connect.connectdb()
            c = conn.cursor()

            #get all starred quotes
            command = f"select * from quotes where uid={ctx.author.id} and star=true"
            print(command)
            c.execute(command)
            print('executed')
            result = c.fetchall()

            #get all quotes like quote
            command = f"select distinct * from quotes where uid={ctx.author.id} and lower(quote) like lower('%{quote}%')"
            print(command)
            c.execute(command)
            print('executed')
            results = c.fetchall()

            if len(results) == 0:
                no_exist = discord.Embed(title=f'<:no:907768020561190983> No quote like "{quote}" found', color=0xff0000)
                msg = await ctx.send(embed=no_exist)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
                return
            elif len(results) > 1:
                no_exist = discord.Embed(title=f'<:no:907768020561190983> Query "{quote}" is too common',description="please give us more of the quote", color=0xff0000)
                msg = await ctx.send(embed=no_exist)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
                return

            else:
                if results[0][5] == True:
                    no_nsfw = discord.Embed(title=f"<:no:907768020561190983> NSFW quotes cannot be added as star quotes", color=0xff0000)
                    msg = await ctx.send(embed=no_nsfw)
                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
                    return

                if len(result) >= 3 and results[0][6] == False:
                    success = discord.Embed(title=f"<:no:907768020561190983> You cannot add more then 3 star quotes", color=0xff0000)
                    msg = await ctx.send(embed=success)
                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
                    return

                if results[0][6] == False:
                    command = f"update quotes set star=True where uid={ctx.author.id} and qid={results[0][0]}"
                    print(command)
                    c.execute(command)
                    print('executed')
                    conn.commit()
                    conn.close()
                    success = discord.Embed(title=f"<a:starry:921635282019831878> Added Starred Quote",description=f'"{results[0][2]}"', color=0x00ff00)
                    msg = await ctx.send(embed=success)
                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
                else:
                    command = f"update quotes set star=False where uid={ctx.author.id} and qid={results[0][0]}"
                    print(command)
                    c.execute(command)
                    print('executed')
                    conn.commit()
                    conn.close()
                    success = discord.Embed(title=f"<a:nostar:921639433013428266> Removed Starred Quote",description=f'"{results[0][2]}"', color=0x00ff00)
                    msg = await ctx.send(embed=success)
                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
        except:
            trace.print_exc()


    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setquotechannel(self, ctx,*,unset=""):
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
        
        conn = connect.connectdb()
        c = conn.cursor()
        command = f"SELECT * FROM channels WHERE guild_id = {ctx.guild.id} and type='quotes'"
        print(command)
        c.execute(command)
        results = c.fetchall()
        print(results)
        if len(results) == 1 and unset.lower()=="none":
            command = f"delete from channels where guild_id = {ctx.guild.id} and type='quotes'"
            print(command)
            c.execute(command)
            conn.commit()
            conn.close()
            await ctx.send(f"Channel <#{ctx.channel.id}> is no longer the quotes channel. Commands are no longer locked to this channel")
        elif len(results) == 0 and unset.lower()=="none":
            await ctx.send(f"No quotechannel is set")
        elif len(results) == 0 and unset.lower()=="":
            command = f"insert into channels(guild_id,channel_id,type) values({ctx.guild.id},{ctx.channel.id},'quotes')"
            print(command)
            c.execute(command)
            conn.commit()
            conn.close()
            await ctx.send(f"Channel <#{ctx.channel.id}> has been set as the quote channel :thumbsup:!\nCommands are now locked to this channel")
        elif len(results)==1 and unset.lower()=="":
            command5 = f"UPDATE channels SET channel_id={ctx.channel.id} where guild_id={ctx.guild.id} and type='quotes';" 
            print(command5)
            c.execute(command5)
            conn.commit()
            conn.close()
            await ctx.send(f"Channel <#{ctx.channel.id}> has been set as the quote channel :thumbsup:!\nCommands are now locked to this channel")
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
            await ctx.send(f"Channel <#{ctx.channel.id}> has been set as the quote channel :thumbsup:!\nCommands are now locked to this channel")
            await warnmsg.delete()
        await ctx.message.delete()
    
    @setquotechannel.error
    async def channel_set_error(self, ctx, error):
        if isinstance(error, MissingPermission):
            await ctx.send(f"Sorry {ctx.author}. You lack permission **Manage Server**")

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
        print(userquotes)
        if len(userquotes) != 0:
            print(len(userquotes))
            randnum = random.randint(0, len(userquotes)-1)
            randquote = userquotes[randnum][2]
            return(randquote)
        else:
            return(None)

    @commands.command()
    async def quote(self, ctx, user: discord.User, *,partquote=None, owo=False):
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
            await ctx.send("A channel error has occured. Please reset your channel again using **q!setquotechannel**")

        if channel == ctx.channel.id or channel==None:

            print("quoting...")
            print(partquote)
            print(f'is owo: {owo}')
            if partquote==None:
                userquote = self.get_rand_quote(self.get_quotes(user.id, ctx.guild.id))
                name = user.name
                print(userquote)
                if userquote is None:
                    if owo==True:
                        no_quote = discord.Embed(title=f'OWNWO!!! {user} has no saved quotes on this server! uwu',description="Pwease add some with **q!addquote <user> <quote>** owo",color=0x0fff23)
                    else:
                        no_quote = discord.Embed(title=f'{user} has no saved quotes on this server!',description="Add some with **q!addquote <user> <quote>**",color=0x0fff23)
                        no_quote.timestamp = datetime.datetime.utcnow()
                        no_quote.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    await ctx.send(embed=no_quote)
                else:

                    if owo==True:

                        await ctx.send(f"OwO <@{user.id}>, <@{ctx.author.id}> is qowoting you UwU <3")
                    embedVar = discord.Embed(title=f'"{userquote}"', color=0xB335C9)
                    embedVar.timestamp = datetime.datetime.utcnow()
                    embedVar.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    embedVar.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)
                    await ctx.send(embed=embedVar)
                    print("quoted")
            else:
                # print('secondary')
                connect = self.bot.get_cog("Misc")
                conn = connect.connectdb()
                c = conn.cursor()
                command = f"SELECT * FROM quotes WHERE uid = {user.id} and guild_id = {ctx.guild.id} and LOWER(quote) like LOWER('%{partquote}%')"
                print(command)
                c.execute(command)
                results = c.fetchall()
                conn.commit()
                conn.close()
                name = user.name
                if len(results) == 0:
                    if owo==True:
                        no_quote = discord.Embed(title=f'OWNWO!!! {user} No quote matches your quewy <3',description=f"Quewy: {partquote}\nPwease make sure the quote u entered exists owo (q!profile <@user/user#0000>)",color=0x0fff23)
                    else:
                        no_quote = discord.Embed(title=f'{user} no quote matches your query!',description=f"Query: {partquote}\nPlease make sure the quote you entered exists (q!profile <@user/user#0000>)",color=0x0fff23)
                        no_quote.timestamp = datetime.datetime.utcnow()
                        no_quote.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")

                    await ctx.send(embed=no_quote)
                elif len(results) > 1:
                    # print('is loong')
                    if owo==True:
                        no_quote = discord.Embed(title=f'OOPSY WOOPSY! That term is too common!',description="This made us make a fucky wucky owo\npwetty pwease could u provide more of the quote for us uwu\nTHWANKS >.< <3\n\nA list of all your fwends qwotes can be fownd using\nq!profile <@fwend/fwend#0000>",color=0x0fff23)
                    else:
                        no_quote = discord.Embed(title=f'The term "{partquote}" is too common!',description="Please provide more of the quote\n\nYou can get a list of a users quote by using\nq!profile <@user/user#0000>",color=0x0fff23)
                        no_quote.timestamp = datetime.datetime.utcnow()
                        no_quote.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    await ctx.send(embed=no_quote)
                else:
                    if owo==True:
                        # print('yes')
                        await ctx.send(f"OwO <@{user.id}>, <@{ctx.author.id}> is qowoting you UwU <3")
                    embedVar = discord.Embed(title=results[0][2], color=0xB335C9)
                    embedVar.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)
                    embedVar.timestamp = datetime.datetime.utcnow()
                    embedVar.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    await ctx.send(embed=embedVar)
                    print("quoted")

        else:
            msg = await ctx.send(f"Quotebot commands are locked to channel <#{results[0][2]}>")
            await asyncio.sleep(5)
            await ctx.message.delete()
            await msg.delete()

    @commands.command()
    async def qowote(self, ctx, user: discord.User,*,quote=None):
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
        # print(f"qowoting: {quote}")
        await self.quote(ctx, user, owo=True, partquote=quote)

    @commands.command()
    async def clean(self, ctx, count):
        if ctx.author.bot == True:
            return
        await ctx.channel.purge(limit=int(count)+1)

    @commands.command()
    async def add50quotes(self, ctx):
        if ctx.author.bot == True:
            return
        try:
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
                tf = [True, False]
                randtf = tf[random.randint(0,1)]
                print(randomword)
                command = f"insert into quotes(uid,quote,date_added,guild_id,nsfw) values(274213987514580993,'test{i}_{randomword}','testing_add', {ctx.guild.id}, {randtf});"
                print(command)
                c.execute(command)
                print("executed")
            conn.commit()
            c.close()
        except:
            trace.print_exc()

    @commands.command()
    async def del50quotes(self, ctx):
        if ctx.author.bot == True:
            return
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


    # ----[Manage quotes: mark nsfw, report, quick-del, etc]----

    # @commands.command()
    # @commands.has_permissions(manage_guild=True)
    # async def manage(self, ctx, user: discord.User, *, gquote=False):
    #     try:

    #         #define misc cog variable
    #         connect = self.bot.get_cog("Misc")
            
    #         try:
    #             blist = await connect.checkblist(ctx, ctx.author)
    #         except:
    #             trace.print_exc()
    #         if blist is not None:
    #             if blist[1]=="global":
    #                 await ctx.send(embed=blist[0])
    #                 return
    #             else:
    #                 pass
    #         else:
    #             pass

    #         #check if gquote is dev
    #         if gquote==True and ctx.author.id!=274213987514580993:
    #             gquote=False

    #         conn = connect.connectdb()
    #         c = conn.cursor()
    #         #change query based on global

    #         if gquote==True:
    #             command = f"SELECT * FROM quotes WHERE uid = {user.id}"
    #         else:
    #             command=f"SELECT * FROM quotes WHERE uid = {user.id} and guild_id = {ctx.guild.id}"

    #         print(command)
    #         c.execute(command)
    #         print("executed")
    #         results = c.fetchall()
    #         command2 = f"select * from users where uid={user.id}"
    #         c.execute(command2)
    #         author = c.fetchall()
    #         conn.commit()

    #         nsfw_q=[]
    #         nsfw_split_quotes=[]
    #         base_q=[]
    #         base_split_quotes=[]
            
    #         # print(results)
    #         for quotes in results:
    #             try:
    #                 if quotes[5]==True:
    #                     nsfw_q.append(quotes[2])
    #                 else:
    #                     base_q.append(quotes[2])
    #             except:
    #                 trace.print_exc()

    #         #seperate quotes into lists of 10 (or a single list if <=10)
    #         if len(base_q) > 9:
    #             base_split_quotes = [base_q[i:i + 9] for i in range(0, len(base_q), 9)]
    #         elif len(base_q) == 0:
    #             pass
    #         else:
    #             base_split_quotes = [base_q]

    #         #seperate nsfw quotes into lists of 10 (or a single list if <=10)
    #         if len(nsfw_q) > 9:
    #             nsfw_split_quotes = [nsfw_q[i:i + 9] for i in range(0, len(nsfw_q), 9)]
    #         elif len(nsfw_q) == 0:
    #             pass
    #         else:
    #             nsfw_split_quotes = [nsfw_q]

    #         print(f"len of base: {len(base_q)}\nlen of split base: {len(base_split_quotes)}\nlen of nsfw {len(nsfw_q)}\nlen of split nsfw: {len(nsfw_split_quotes)}")

    #         bio = str(author[0][8])

    #         #check if user is NSFW locked
    #         if author[0][2] == True: 
    #             actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0"),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]
    #         elif author[0][2] == False:
    #             actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0", disabled=True),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]

    #         #create profile page
    #         manage_page = discord.Embed(title=f"{user}'s Profile", description=f"Bio: {bio}\n\n-", color=0x54de99)
    #         manage_page.set_thumbnail(url=user.avatar_url)

    #         #add up to 3 star quotes
    #         command = f"select * from quotes where uid={user.id} and star=True"
    #         print(command)
    #         c.execute(command)
    #         print('executed')
    #         star_q = c.fetchall()
    #         if len(star_q)!=0:
    #             for quote in star_q:
    #                 manage_page.add_field(name=f'<:Star:907780904221552661> "{quote[2]}"', value=f"-{user.name}", inline=True)
    #         else:
    #             manage_page.add_field(name=f" \n<:Star:907780904221552661> No star quotes yet", value=f"add up to 3 with **q!star add <part-of-quote>**")
    #         conn.close()

    #         base_pages = []
    #         nsfw_pages = []

    #         #Dev
    #         if gquote == True:
    #             server = "Global"
    #         else:
    #             server = ctx.guild.name

    #         #check if user has quotes
            

    #         #create non-nsfw quote pages
    #         i = 1
    #         if len(base_split_quotes)==0:
    #             page_embed = discord.Embed(title=f"{user} has no quotes for this server", description=f"Add some with **q!add <@user/user#0000> <quote>**", color=0xff4f42)
    #             page_embed.timestamp = datetime.datetime.utcnow()
    #             page_embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
    #             base_pages.append(page_embed)

    #         else:
    #             base_buttons = []
    #             for page in base_split_quotes:
    #                 page_embed = discord.Embed(title=f"Quotes for {user} (Page {i}/{len(base_split_quotes)})", description=f"from server {server}", color=0x54de99)
    #                 buttons = []
    #                 i2 = 1
    #                 for quote in page:
    #                     page_embed.add_field(name=f'[{i2}] {quote}',value=f"-{user.name}", inline=True)
    #                     buttons.append(Button(label=f"{i2}", style=1, custom_id=f"qmanage_base_{i}_{i2}_{user.id}",disabled=True))
    #                     i2 += 1
    #                 button_cfg = [[buttons[i:i + 3] for i in range(0, len(base_q), 3)], Button(label="Back", style=3, custom_id=f"blank_back_for_manage")]
    #                 page_embed.timestamp = datetime.datetime.utcnow()
    #                 page_embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            
    #                 base_pages.append(page_embed)
    #                 base_buttons.append(button_cfg)
    #                 i+=1
                    

    #         #create nsfw pages
    #         i = 1
    #         if len(nsfw_split_quotes)==0:
    #             page_embed = discord.Embed(title=f"{user} has no nsfw quotes for this server", description=f"Manually mark quotes as nsfw with **q!nsfw <@user/user#0000> <part-of-quote>**", color=0xff4f42)
    #             page_embed.timestamp = datetime.datetime.utcnow()
    #             page_embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")                
    #             nsfw_pages.append(page_embed)
    #         else:
    #             nsfw_buttons = []
    #             for page in nsfw_split_quotes:
    #                 page_embed = discord.Embed(title=f"NSFW Quotes for {user} (Page {i}/{len(base_split_quotes)})", description=f"from server {server}", color=0x54de99)
    #                 buttons = []
    #                 i2 = 1
    #                 for quote in page:
    #                     page_embed.add_field(name=f'{quote}',value=f"-{user.name}", inline=True)
    #                     buttons.append(Button(label=f"{i2}", style=1, custom_id=f"qmanage_nsfw_{i}_{i2}_{user.id}",disabled=True))
    #                     i2 += 1

    #                 button_cfg = [[buttons[i:i + 3] for i in range(0, len(base_q), 3)], Button(label="Back", style=3, custom_id=f"blank_back_for_manage")]
    #                 nsfw_buttons.append(button_cfg)

    #                 page_embed.timestamp = datetime.datetime.utcnow()
    #                 page_embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
    #                 nsfw_pages.append(page_embed)
    #                 i+=1

    #         print(base_buttons)
    #         print(nsfw_buttons)
        
    #         #send initial manage menu (its just profile)
    #         manage_page.timestamp = datetime.datetime.utcnow()
    #         manage_page.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
    #         msg = await ctx.send(embed=manage_page,components=[actions])

    #         # command = f'update users set profile_cooldown=t'

    #         def check(x):
    #             return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id and x.message.id == msg.id and x.message.id == msg.id and x.message.id == msg.id

    #         #check for button responses
    #         try:
    #             response = await self.bot.wait_for("button_click", check=check, timeout=120)
    #             await response.respond(type=6)
    #             await self.manage_menu(ctx, msg, author, user, manage_page, base_pages, nsfw_pages, response, base_buttons,nsfw_buttons)

    #         #delete if timeout
    #         except asyncio.exceptions.TimeoutError:
    #             await msg.delete()
    #             await ctx.message.delete()
    #             return

    #     except:
    #         trace.print_exc()

    # async def manage_menu(self, ctx, msg, author, user, profile, base, nsfw, response, base_buttons, nsfw_buttons):
    #     if "uquotes_" in str(response.custom_id):
    #         if "uquotes_base" in str(response.custom_id):
    #             intid=str(response.custom_id).replace("uquotes_base_","")
    #             page = intid[0]

    #             next_page = base[int(page)]

    #             if int(page) == 0:
    #                 print(base_buttons[int(page)])
    #                 actions = [[Button(label="Back", style=2, custom_id=f"uquotes_base_{int(page)-1}_{user.id}",disabled=True),Button(label="Next", style=3, custom_id=f"uquotes_base_{int(page)+1}_{user.id}")],[[[base_buttons[int(page)]]]],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             elif int(page) == len(base)-1:
    #                 actions = [[Button(label="Back", style=3, custom_id=f"uquotes_base_{int(page)-1}_{user.id}"),Button(label="Next", style=2, custom_id=f"uquotes_base_{int(page)+1}_{user.id}", disabled=True)],base_buttons[int(page)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             else:
    #                 actions = [[Button(label="Back", style=3, custom_id=f"uquotes_base_{int(page)-1}_{user.id}"),Button(label="Next", style=3, custom_id=f"uquotes_base_{int(page)+1}_{user.id}")],base_buttons[int(page)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             if len(base)-1 == 0:
    #                 actions = [[Button(label="Back", style=2, custom_id=f"uquotes_base_{int(page)-1}_{user.id}", disabled=True),Button(label="Next", style=2, custom_id=f"uquotes_base_{int(page)+1}_{user.id}", disabled=True)],base_buttons[int(page)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             await msg.edit(embed=next_page, components=actions)
                

    #         elif "uquotes_nsfw" in str(response.custom_id):
    #             intid=str(response.custom_id).replace("uquotes_nsfw_","")
    #             page = intid[0]

    #             next_page = nsfw[int(page)]

    #             if int(page) == 0:
    #                 actions = [[Button(label="Back", style=2, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}",disabled=True),Button(label="Next", style=3, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}")],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             elif int(page) == len(base)-1:
    #                 actions = [[Button(label="Back", style=3, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}"),Button(label="Next", style=2, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}", disabled=True)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             else:
    #                 actions = [[Button(label="Back", style=3, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}"),Button(label="Next", style=3, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}")],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             if len(nsfw)-1 == 0:
    #                 actions = [[Button(label="Back", style=2, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}", disabled=True),Button(label="Next", style=2, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}", disabled=True)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #             await msg.edit(embed=next_page, components=actions)
    #         else:   
    #             pass

    #     if "qmanage_" in str(response.custom_id):
    #         quotes = {'base': base, 'nsfw':nsfw}
    #         ids = str(response.custom_id).split("_")
    #         qtype = ids[2]
    #         page = ids[3]
    #         quote = ids[4]
            
    #         final = quotes[f'{qtype}'][page][quote]

    #         manage_embed = discord.Embed(title=f"Managing Quote {quote} of {user}", description=f"Managing quote {qtype}.{page}.{quote}")
    #         manage.add_field(name=f"{final}", value=f"-")
    #         embedVar.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)

    #         if qtype == 'base':
    #             styles=3
    #         elif qtype == 'nsfw':
    #             syles=4

    #         actions = [[Button(label="Toggle NSFW", style=styles, custom_id=f"nsfwtoggle_{page}_{quote}_{user.id}", disabled=True),Button(label="Remove", style=4, custom_id=f"qremove_{page}_{quote}_{user.id}", disabled=True),Button(label="QRUMBL", style=4, custom_id=f"qrmbl_{user.id}", disabled=True)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
    #         await msg.edit(embed=next_page, components=actions)

    #     elif "blist_global" in str(response.custom_id):
    #         pass

    #     elif "profile_" in str(response.custom_id):
    #         if author[0][2] == True: 
    #             actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0"),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]
    #         elif author[0][2] == False:
    #             actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0", disabled=True),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]
    #         await msg.edit(embed=profile, components=[actions])

    #     def check(x):
    #         return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id and x.message.id == msg.id
    #     try:
    #         response = await self.bot.wait_for("button_click", check=check, timeout=120)
    #         await response.respond(type=6)
    #         await self.profile_menu(ctx, msg, author, user, profile, base, nsfw, response)
    #     except asyncio.exceptions.TimeoutError:
    #         await msg.delete()
    #         await ctx.message.delete()
    #         return

    async def is_nsfw(self, ctx, quote, user):
        #filter API for quotes if no slurs found
        # quote = quote.replace(" ", "%")

        async def api(ctx, quote):
            print(f"\nCURRENT API CALL: {quote}\n")
            url = 'https://api.sightengine.com/1.0/text/check.json'

            data =  {
            'text':f'{quote}',
            'lang':'en',
            'list':'tli_aTs79afVyEDmo23PBJtBc',
            'mode':'standard',
            'api_user':f'1577683888',
            'api_secret':'KwUgHawuH53aRMPntbQA'
            }

            response = requests.post(url, data=data)

            response = response.json()
            print(response)
            return response
            

        async def blacklist_check(ctx, blacklist, i):
            try:
                if blacklist[i]['match'] == "rape" or blacklist[i]['match'] == "raped":
                    return True, False, False, f"Sexual Harassment ('{blacklist[i]['match']}')"

                elif blacklist[i]['match'] == "retarded":
                    return True, False, False, f"Derogatory ('{blacklist[i]['match']}')"

                elif blacklist[i]['match'] == "nazi":
                    return True, False, False, f"Sensitive Topic ('{blacklist[i]['match']}')"
                    
                else:
                    return None
            except:
                trace.print_exc()

        response = await api(ctx, quote)

        profanity = response['profanity']['matches']
        blacklist = response['blacklist']['matches']
        personal = response['personal']['matches']
        link = response['link']['matches']

        # >> RETURN(NSFW, REVIEW, CANCEL, REASON) <<

        if len(personal) != 0:
            return False, True, True, f"Personal Information Detected ('{personal[0]['type']}')"
        
        if len(link) != 0:
            return False, False, True, "link"

        if len(profanity) != 0:
            for i in range(len(profanity)):
                if profanity[i]['type'] == 'discriminatory':
                    return True, True, False, f"Discrimination ('{profanity[i]['match']}')"

                elif profanity[i]['type'] == 'derogatory':
                    return True, True, False, f"Derogatory ('{profanity[i]['match']}')"

                else:
                    print('nothing passing...')

            if len(blacklist) != 0:
                for i in range(len(blacklist)):
                    blist_check = await blacklist_check(ctx, blacklist, i)
                    if blist_check != None:
                        return blist_check
                    else:
                        pass

            else:
                print('blacklist is empty')
                return False, False, False, "None"

        else:
            print('profan is empt')
            if len(blacklist) != 0:
                for i in range(len(blacklist)):
                    blist_check = await blacklist_check(ctx, blacklist, i)
                    if blist_check != None:
                        return blist_check
                    else:
                        pass


            else:
                print('blacklith no')
                return False, False, False, "None"

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        # await interaction.respond(type=6)
        try:
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            if interaction.custom_id == "passq":
                action = f"**Reviewed: Allowed/Ignored**"

            elif "rmq_" in interaction.custom_id:
                command=f'delete from quotes where qid={str(interaction.custom_id).replace("rmq_","")}'
                c.execute(command)
                action = f"**Reviewed: Quote Removed**"

            elif "rmb_" in interaction.custom_id:
                new_id = str(interaction.custom_id).split("_")
                command=f'delete from quotes where qid={str(interaction.custom_id).replace("rmq_","")}'
                c.execute(command)
                command=f"update users set global_blist=True where uid={new_id[2]}"
                c.execute(command)
                command=f"update users set blist_reason='Blacklisted by Reviewer' where uid={new_id[2]}"
                c.execute(command)
                action = f"**Reviewed: Quote Removed + User {new_id[2]} Blacklisted**"

            elif "block_" in interaction.custom_id:
                new_id = str(interaction.custom_id).split("_")
                command=f"update users set global_blist=True where uid={new_id[1]}"
                c.execute(command)
                command=f"update users set blist_reason='Blacklisted by Reviewer' where uid={new_id[1]}"
                c.execute(command)
                action = f"**Reviewed: User {new_id[2]} Blacklisted**"

            else:
                return
            conn.commit()
            conn.close()
            await interaction.message.edit(content=f"{action}", components=[])
        except:
            trace.print_exc()


    async def review_send(self, ctx, quote, qid, nsfw, user, blocked):
        support_server = self.bot.get_guild(id=838814770537824378)
        dev = support_server.get_channel(918652952955219968)
        embed = discord.Embed(title=f"Quote review required", description=f'**Added to user:** {user} | ID: {user.id}\n**Quote:** {quote}\n**Review Reason:** {nsfw[3]}\n\n------------------------------------------------------------------------------------------', color=0x00ff00)
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        c = conn.cursor()
        command = f"select quote from quotes where uid='{ctx.author.id}' and nsfw=false"
        print(command)
        c.execute(command)
        result = c.fetchall()
        command = f"select quote from quotes where uid='{ctx.author.id}' and nsfw=true"
        print(command)
        c.execute(command)
        result2 = c.fetchall()
        command = f"select quote from quotes where guild_id={ctx.guild.id}"
        print(command)
        c.execute(command)
        result3 = c.fetchall()
        c.close()
        embed.add_field(name="Server Info:", value=f"**Name:** {ctx.guild.name}\n**ID:** {ctx.guild.id}\n**Members:** {len(ctx.guild.members)}\n**Quotes:** {len(result3)}", inline=True)
        embed.add_field(name="User Info:", value=f"**Name:** {ctx.author}\n**ID:** {ctx.author.id}\n**bQuotes:** {len(result)}\n**nQuotes:** {len(result2)}", inline=True)
        embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
        embed.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        if blocked!=True:
            actions = [Button(label=f"Allow",emoji=self.bot.get_emoji(892331857440559124), style=3, custom_id=f"passq"),Button(label=f"Remove",emoji=self.bot.get_emoji(892436376673464340), style=4, custom_id=f"rmq_{qid}"),Button(label=f"RM+Block",emoji=self.bot.get_emoji(921550189225980025), style=4, custom_id=f"rmb_{qid}_{ctx.author.id}")]
        elif blocked==True:
            actions = [Button(label=f"Ignore",emoji=self.bot.get_emoji(921570927291007047), style=2, custom_id=f"passq"),Button(label=f"Block",emoji=self.bot.get_emoji(921550189225980025), style=4, custom_id=f"block_{ctx.author.id}")]
        else:
            print(f'invalid review block status response | id:{user.id} | gid: {ctx.guild.id}')
            return

        await dev.send(embed=embed,components=[actions])


    @commands.command(aliases=['+','create','make','addquote'])
    async def add(self, ctx, user: discord.User,*,quote=""):
        if ctx.author.bot == True:
            return
        dbquote = quote.replace("'", "''")
        #check if user is blacklisted
        try:

            #define misc cog variable
            connect = self.bot.get_cog("Misc")
            
            try:
                blist = await connect.checkblist(ctx, ctx.author)
            except:
                trace.print_exc()
            if blist is not None:
                if blist[1]=="global":
                    await ctx.send(embed=blist[0])
                    return
                else:
                    pass
            else:
                pass
            
            if user.bot == True:
                no_bot = discord.Embed(title=f"Quotes cannot be added to Bots", color=0xff0000)
                msg = await ctx.send(embed=no_bot)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
                return

            if quote=="":
                no_quote = discord.Embed(title=f'Please provide a quote to add',color=0x0fff23)
                no_quote.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                msg = await ctx.send(embed=no_quote)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
                return

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
                await ctx.send("A channel error has occured. Please reset your quote channel again using **q!setquotechannel**")

            if channel == ctx.channel.id or channel==None:

                if len(quote) > 250:
                    embed = discord.Embed(title="Your quote is too long! We only allow quote of up to 250 characters", color=0xff0000)
                    embed.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                    msg = await ctx.send(embed=embed)
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                    await msg.delete()
                    return

                conn = connect.connectdb()
                c = conn.cursor()
                command = f"select * from quotes where uid={user.id} and guild_id={ctx.guild.id} and lower(quote) like lower('%{dbquote}%')"
                print(command)
                c.execute(command)
                print('executed')
                results = c.fetchall()

                if len(results)!=0:

                    no_quote = discord.Embed(title=f'Quote Already exists',description=f'This server already has that quote for that user',color=0x0fff23)
                    no_quote.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                    msg = await ctx.send(embed=no_quote)
                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
                    return

                else:
                    dupe_q = ""
                    if ctx.author.id == user.id:
                        dupe_q = f""
                    confirm_embed = discord.Embed(title="Please confirm the quote you wish to add", description=f"{dupe_q}", color=0x00ff00)
                    actions = []
                    
                    confirm_embed.add_field(name=f'"{quote}"',value=f"-{user.name}")
                    confirm_embed.timestamp = datetime.datetime.utcnow()
                    confirm_embed.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")


                    button = Button(label=f"Confirm", style=3, custom_id=f"add_quote")
                    actions.append(button)


                    actions.append(Button(label="Cancel", style=4, custom_id=f"add_cancel"))

                    nsfw = await self.is_nsfw(ctx, quote, user)
                    print(nsfw)

                    if nsfw[0] == True and nsfw[1]==True:
                        msg = f"<:Warning:909946407673274398> **This quote has been flagged for review** (q!review)"
                        review = True
                    elif nsfw[0]==True and nsfw[1]==False:
                        msg = f"<:Warning:909946407673274398> **This quote has been Automarked as NSFW** (q!nsfw)"
                        review = False
                    else:
                        review = False
                        msg=None


                    if nsfw[2] == True:
                        if nsfw[1] == True:
                            quote_canceled = discord.Embed(title=f"<:redx:891428508868435998> Quote Blocked", description="Your quote has been blocked from being added and has been sent in for review\nLearn More:** q!blocked**", color=0xff0000)
                            quote_canceled.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                            message = await ctx.send(embed=quote_canceled)
                            qid=None
                            await self.review_send(ctx, quote, qid, nsfw, user, True)
                            await asyncio.sleep(20)
                            await message.delete()
                            await ctx.message.delete()
                            return
                        else:
                            quote_canceled = discord.Embed(title=f"<:redx:891428508868435998> Quote Blocked", description="Your quote has been blocked from being added\nLearn More:** q!blocked**", color=0xff0000)
                            quote_canceled.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                            message = await ctx.send(embed=quote_canceled)
                            await asyncio.sleep(20)
                            await message.delete()
                            await ctx.message.delete()
                            return

                    else:
                        message = await ctx.send(content=msg,embed=confirm_embed,components=[actions])

                    def check(x):
                        return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id and x.message.id == message.id
                    try:
                        response = await self.bot.wait_for("button_click", check=check, timeout=30)
                    
                    except asyncio.exceptions.TimeoutError:
                        await message.delete()
                        await ctx.message.delete()
                        return

                    if response.custom_id == "add_cancel":
                        cancel_embed=discord.Embed(title="Canceled",color=0xff0000)
                        await message.edit(content="",embed=cancel_embed, components=[])
                        await asyncio.sleep(5)
                        await message.delete()
                        await ctx.message.delete()

                    elif "add_quote" in response.custom_id:
                        # nsfw=False
                        command = f"insert into quotes(uid, quote, date_added, guild_id, nsfw, star, added_by, message) values({user.id}, '{dbquote}','{datetime.datetime.now().strftime('%d/%m/%Y')}',{ctx.guild.id},{nsfw[0]},False, {ctx.author.id}, {message.id})"
                        c.execute(command)
                        conn.commit()
                        donemessage = discord.Embed(title=f"\"{quote}\"", color=0x00ff2f)
                        donemessage.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)
                        donemessage.timestamp = datetime.datetime.utcnow()
                        donemessage.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                        await ctx.message.delete()
                        await message.edit(content="", embed=donemessage, components=[])
                        if review==True:
                            command = f"select * from quotes where uid={user.id} and quote='{quote}' and guild_id={ctx.guild.id}"
                            c.execute(command)
                            qid = c.fetchall()
                            qid = qid[0][0]
                            await self.review_send(ctx, quote, qid, nsfw, user, False)
                        conn.close()
                        log = self.bot.get_cog("Logger")
                        await log.logger(title=f"**Quote Added**", desc=f'**"{quote}"**\n\n**To:** {user}\n**By:** {ctx.author}', user=ctx.guild, color="#8dd47d", guild=ctx.guild.id, image=user.avatar_url)

            else:
                msg = await ctx.send(f"Quotebot commands are locked to channel <#{results[0][2]}>")
                await asyncio.sleep(5)
                await ctx.message.delete()
                await msg.delete()

        except:
            trace.print_exc()

    @commands.command(aliases=['rm','del','remove','delquote', '-'])
    async def delete(self, ctx, user: discord.User, *, quote=""):
        if ctx.author.bot == True:
            return
        #check if user is blacklisted
        try:

            #define misc cog variable
            connect = self.bot.get_cog("Misc")
            
            try:
                blist = await connect.checkblist(ctx, ctx.author)
            except:
                trace.print_exc()
            if blist is not None:
                if blist[1]=="global":
                    await ctx.send(embed=blist[0])
                    return
                else:
                    pass
            else:
                pass

            if user.bot == True:
                no_bot = discord.Embed(title=f"Quotes cannot be added to Bots", color=0xff0000)
                no_bot.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                msg = await ctx.send(embed=no_bot)
                await asyncio.sleep(5)
                await msg.delete()
                await ctx.message.delete()
                return

            if quote=="":
                no_quote = discord.Embed(title=f'Please provide a quote to delete!',color=0x0fff23)
                no_quote.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                msg = await ctx.send(embed=no_quote)
                await asyncio.sleep(5)
                await msg.delete()
                return

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
                await ctx.send("A channel error has occured. Please reset your quote channel again using **q!setquotechannel**")

            if channel == ctx.channel.id or channel==None:
                conn = connect.connectdb()
                c = conn.cursor()
                command = f"select * from quotes where uid={user.id} and guild_id={ctx.guild.id} and LOWER(quote) like LOWER('%{quote}%')"
                print(command)
                c.execute(command)
                print('executed')
                results = c.fetchall()

                if len(results) > 3:
                    no_quote = discord.Embed(title=f'The term "{quote}" is too common!',description="Please provide more of the quote",color=0x0fff23)
                    no_quote.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                    msg = await ctx.send(embed=no_quote)
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                    await msg.delete()
                    return

                elif len(results)==0: 
                    no_quote = discord.Embed(title=f'No quote like "{quote}" found!',color=0x0fff23)
                    no_quote.set_author(name=ctx.author, url=discord.Embed.Empty, icon_url=ctx.author.avatar_url)
                    msg = await ctx.send(embed=no_quote)
                    await asyncio.sleep(5)
                    await ctx.message.delete()
                    await msg.delete()
                    return

                else:
                    confirm_embed = discord.Embed(title="Please confirm the quote you wish to delete", description="This action cannot be undone\n----", color=0xd92b1e)
                    actions = []

                    i = 1

                    for quote in results:
                        confirm_embed.add_field(name=f'"{quote[2]}"',value=f"-{user.name}")
                        button = Button(label=f"Confirm {i}", style=3, custom_id=f"delete_quote_{i}")
                        actions.append(button)
                        i+=1

                    actions.append(Button(label="Cancel", style=4, custom_id=f"delete_cancel"))

                    msg = await ctx.send(embed=confirm_embed, components=[actions])

                    def check(x):
                        return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id and x.message.id == msg.id and x.message.id == msg.id and x.message.id == msg.id
                    try:
                        response = await self.bot.wait_for("button_click", check=check,timeout=30)
                    
                    except asyncio.exceptions.TimeoutError:
                        await msg.delete()
                        await ctx.message.delete()
                        return

                    if response.custom_id == "delete_cancel":
                        cancel_embed=discord.Embed(title="Canceled",color=0xff0000)
                        await msg.edit(content="",embed=cancel_embed, components=[])

                    elif "delete_quote" in response.custom_id:
                        quote = int(str(response.custom_id).replace("delete_quote_", ""))
                        qid = results[quote-1][0]
                        command = f"delete from quotes where qid={qid}"
                        c.execute(command)
                        conn.commit()
                        conn.close()
                        complete_embed=discord.Embed(title="<:yes:892537190347837450> Succesfully Deleted Quote",description=f'"{results[quote-1][2]}"\n-{user.name}', color=0x00ff00)
                        await msg.edit(embed=complete_embed, components=[])
                    log = self.bot.get_cog("Logger")
                    await log.logger(title=f"**Quote Deleted**", desc=f'**"{results[quote-1][2]}"**\n\n**From:** {user}\n**By:** {ctx.author}', user=ctx.guild, color="#DE6363", guild=ctx.guild.id, image=user.avatar_url)

                    await asyncio.sleep(5)
                    await msg.delete()
                    await ctx.message.delete()
                    

            else:
                msg = await ctx.send(f"Quotebot commands are locked to channel <#{results[0][2]}>")
                await asyncio.sleep(5)
                await ctx.message.delete()
                await msg.delete()


        except:
            trace.print_exc()

    @commands.command(aliases=['who','listquotes','list','quotes','ls', 'show', '?'])
    async def profile(self, ctx, user: discord.User, gquote=False):

        #check if user is blacklisted
        try:

            #define misc cog variable
            connect = self.bot.get_cog("Misc")
            
            try:
                blist = await connect.checkblist(ctx, ctx.author)
            except:
                trace.print_exc()
            if blist is not None:
                if blist[1]=="global":
                    await ctx.send(embed=blist[0])
                    return
                else:
                    pass
            else:
                pass

            #check if gquote is dev
            if gquote==True and ctx.author.id!=274213987514580993:
                gquote=False

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
                await ctx.send("A channel error has occured. Please reset your quote channel again using **q!setquotechannel**")

            if channel == ctx.channel.id or channel==None:

                #change query based on global
                if gquote==True:
                    command = f"SELECT * FROM quotes WHERE uid = {user.id}"
                else:
                    command=f"SELECT * FROM quotes WHERE uid = {user.id} and guild_id = {ctx.guild.id}"

                print(command)
                c.execute(command)
                print("executed")
                results = c.fetchall()
                command2 = f"select * from users where uid={user.id}"
                c.execute(command2)
                author = c.fetchall()
                conn.commit()

                nsfw_q=[]
                nsfw_split_quotes=[]
                base_q=[]
                base_split_quotes=[]
                
                # print(results)
                for quotes in results:
                    try:
                        if quotes[5]==True:
                            nsfw_q.append(quotes[2])
                        else:
                            base_q.append(quotes[2])
                    except:
                        trace.print_exc()

                #seperate quotes into lists of 10 (or a single list if <=10)
                if len(base_q) > 9:
                    base_split_quotes = [base_q[i:i + 9] for i in range(0, len(base_q), 9)]
                elif len(base_q) == 0:
                    pass
                else:
                    base_split_quotes = [base_q]

                #seperate nsfw quotes into lists of 10 (or a single list if <=10)
                if len(nsfw_q) > 9:
                    nsfw_split_quotes = [nsfw_q[i:i + 9] for i in range(0, len(nsfw_q), 9)]
                elif len(nsfw_q) == 0:
                    pass
                else:
                    nsfw_split_quotes = [nsfw_q]

                print(f"len of base: {len(base_q)}\nlen of split base: {len(base_split_quotes)}\nlen of nsfw {len(nsfw_q)}\nlen of split nsfw: {len(nsfw_split_quotes)}")

                bio = str(author[0][8])

                #check if user is NSFW locked
                if author[0][2] == True: 
                    actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0"),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]
                elif author[0][2] == False:
                    actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0", disabled=True),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]

                #create profile page
                profile_page = discord.Embed(title=f"{user}'s Profile", description=f"Bio: {bio}\n\n-", color=0x54de99)
                profile_page.set_thumbnail(url=user.avatar_url)

                #add up to 3 star quotes
                command = f"select * from quotes where uid={user.id} and star=True"
                print(command)
                c.execute(command)
                print('executed')
                star_q = c.fetchall()
                if len(star_q)!=0:
                    for quote in star_q:
                        profile_page.add_field(name=f'<:Star:907780904221552661> "{quote[2]}"', value=f"-{user.name}", inline=True)
                else:
                    profile_page.add_field(name=f" \n<:Star:907780904221552661> No star quotes yet", value=f"add up to 3 with **q!star <part-of-quote>**")
                conn.close()

                base_pages = []
                nsfw_pages = []

                #Dev
                if gquote == True:
                    server = "Global"
                else:
                    server = ctx.guild.name

                #check if user has quotes
                

                #create non-nsfw quote pages
                i = 1
                if len(base_split_quotes)==0:
                    page_embed = discord.Embed(title=f"{user} has no quotes for this server", description=f"Add some with **q!add <@user/user#0000> <quote>**", color=0xff4f42)
                    page_embed.timestamp = datetime.datetime.utcnow()
                    page_embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    base_pages.append(page_embed)

                else:
                    for page in base_split_quotes:
                        page_embed = discord.Embed(title=f"Quotes for {user} (Page {i}/{len(base_split_quotes)})", description=f"from server {server}", color=0x54de99)
                        for quote in page:
                            page_embed.add_field(name=f'{quote}',value=f"-{user.name}", inline=True)
                        base_pages.append(page_embed)
                        i+=1

                #create nsfw pages
                i = 1
                if len(nsfw_split_quotes)==0:
                    page_embed = discord.Embed(title=f"{user} has no nsfw quotes for this server", description=f"If QuoteBot or our team detects any they will be placed here", color=0xff4f42)
                    page_embed.timestamp = datetime.datetime.utcnow()
                    page_embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")                
                    nsfw_pages.append(page_embed)
                else:
                    for page in nsfw_split_quotes:
                        page_embed = discord.Embed(title=f"NSFW Quotes for {user} (Page {i}/{len(base_split_quotes)})", description=f"from server {server}", color=0x54de99)
                        for quote in page:
                            page_embed.add_field(name=f'{quote}',value=f"-{user.name}", inline=True)
                        page_embed.timestamp = datetime.datetime.utcnow()
                        page_embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                        nsfw_pages.append(page_embed)
                        i+=1
            
                #send initial profile menu
                profile_page.timestamp = datetime.datetime.utcnow()
                profile_page.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                msg = await ctx.send(embed=profile_page,components=[actions])
                command = f'update users set profile_cooldown=t'

                def check(x):
                    return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id and x.message.id == msg.id and x.message.id == msg.id and x.message.id == msg.id

                #check for button responses
                try:
                    response = await self.bot.wait_for("button_click", check=check, timeout=120)
                    await response.respond(type=6)
                    await self.profile_menu(ctx, msg, author, user, profile_page, base_pages, nsfw_pages, response)

                #delete if timeout
                except asyncio.exceptions.TimeoutError:
                    await msg.delete()
                    await ctx.message.delete()
                    return
            else:
                msg = await ctx.send(f"Quotebot commands are locked to channel <#{results[0][2]}>")
                await asyncio.sleep(5)
                await ctx.message.delete()
                await msg.delete()

        except:
            trace.print_exc()

    async def profile_menu(self, ctx, msg, author, user, profile, base, nsfw, response):
        if "uquotes_" in str(response.custom_id):
            if "uquotes_base" in str(response.custom_id):
                intid=str(response.custom_id).replace("uquotes_base_","")
                page = intid[0]

                next_page = base[int(page)]

                if int(page) == 0:
                    actions = [[Button(label="Back", style=2, custom_id=f"uquotes_base_{int(page)-1}_{user.id}",disabled=True),Button(label="Next", style=3, custom_id=f"uquotes_base_{int(page)+1}_{user.id}")],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                elif int(page) == len(base)-1:
                    actions = [[Button(label="Back", style=3, custom_id=f"uquotes_base_{int(page)-1}_{user.id}"),Button(label="Next", style=2, custom_id=f"uquotes_base_{int(page)+1}_{user.id}", disabled=True)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                else:
                    actions = [[Button(label="Back", style=3, custom_id=f"uquotes_base_{int(page)-1}_{user.id}"),Button(label="Next", style=3, custom_id=f"uquotes_base_{int(page)+1}_{user.id}")],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                if len(base)-1 == 0:
                    actions = [[Button(label="Back", style=2, custom_id=f"uquotes_base_{int(page)-1}_{user.id}", disabled=True),Button(label="Next", style=2, custom_id=f"uquotes_base_{int(page)+1}_{user.id}", disabled=True)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                await msg.edit(embed=next_page, components=actions)
                

            elif "uquotes_nsfw" in str(response.custom_id):
                intid=str(response.custom_id).replace("uquotes_nsfw_","")
                page = intid[0]

                next_page = nsfw[int(page)]

                if int(page) == 0:
                    actions = [[Button(label="Back", style=2, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}",disabled=True),Button(label="Next", style=3, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}")],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                elif int(page) == len(base)-1:
                    actions = [[Button(label="Back", style=3, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}"),Button(label="Next", style=2, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}", disabled=True)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                else:
                    actions = [[Button(label="Back", style=3, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}"),Button(label="Next", style=3, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}")],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                if len(nsfw)-1 == 0:
                    actions = [[Button(label="Back", style=2, custom_id=f"uquotes_nsfw_{int(page)-1}_{user.id}", disabled=True),Button(label="Next", style=2, custom_id=f"uquotes_nsfw_{int(page)+1}_{user.id}", disabled=True)],[Button(label="Menu", style=1, custom_id=f"profile_{user.id}")]]
                await msg.edit(embed=next_page, components=actions)
            else:   
                pass

        elif "blist_global" in str(response.custom_id):
            pass

        elif "profile_" in str(response.custom_id):
            if author[0][2] == True: 
                actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0"),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]
            elif author[0][2] == False:
                actions = [Button(label="Quotes", style=3, custom_id=f"uquotes_base_0"),Button(label="NSFW", style=4, custom_id=f"uquotes_nsfw_0", disabled=True),Button(label="Badges (Soon)", style=2, custom_id=f"user_badges_{user.id}", disabled=True)]
            await msg.edit(embed=profile, components=[actions])

        def check(x):
            return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id and x.message.id == msg.id
        try:
            response = await self.bot.wait_for("button_click", check=check, timeout=120)
            await response.respond(type=6)
            await self.profile_menu(ctx, msg, author, user, profile, base, nsfw, response)
        except asyncio.exceptions.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
            return

    @commands.command()
    async def togglensfw(self, ctx):
        try:

            #define misc cog variable
            connect = self.bot.get_cog("Misc")
            
            try:
                blist = await connect.checkblist(ctx, ctx.author)
            except:
                trace.print_exc()
            if blist is not None:
                if blist[1]=="global":
                    await ctx.send(embed=blist[0])
                    return
                else:
                    pass
            else:
                pass

            conn = connect.connectdb()
            c = conn.cursor()
            command = f"select * from users where uid={ctx.author.id}"
            print(command)
            c.execute(command)
            print("Executed")
            results=c.fetchall()

            if results[0][2] == True:
                command = f'update users set nsfw=False where uid={ctx.author.id}' 
                c.execute(command)
                conn.commit()
                msg = discord.Embed(title="<:redTick:892436376673464340> You are no longer able to see NSFW content", color=0xff0000)
                message = await ctx.send(embed=msg)
                await asyncio.sleep(5)
                await message.delete()
                await ctx.message.delete()
                

            elif results[0][2]==False:
                command = f'update users set nsfw=True where uid={ctx.author.id}'
                c.execute(command)
                conn.commit()
                msg = discord.Embed(title="<:rbcheck:892331857440559124> You are now able to see NSFW content", color=0x00ff00)
                message = await ctx.send(embed=msg)
                await asyncio.sleep(5)
                await message.delete()
                await ctx.message.delete()

            else:
                print('invalid nsfw result')
                return
            
            conn.close()

        except:
            trace.print_exc()


#-------------------------NSFW CHECKER-------------------------
#     @commands.command()
#     async def nsfwstart(self, ctx):
#         try:
#             connect = self.bot.get_cog("Misc")
#             conn = connect.connectdb()
#             c = conn.cursor()
#             command = f"SELECT * FROM quotes where nsfw is Null"
#             c.execute(command)
#             results = c.fetchall()
#             i=0
#             for quotes in results:
#                 await asyncio.sleep(0.5)
#                 await ctx.send(f"{quotes[2]} [{i}]", components=[[Button(label="Yes", style=3, custom_id=f"nsfw_yes_{quotes[0]}"),Button(label="No", style=4, custom_id=f"nsfw_no_{quotes[0]}")]])
#                 print(i)
#                 i+=1
#         except:
#             trace.print_exc()

# # NSFW CHECKER LISTENER
#     @commands.Cog.listener()
#     async def on_button_click(self, interaction):
#         await interaction.respond(type=6)
#         try:
#             connect = self.bot.get_cog("Misc")
#             conn = connect.connectdb()
#             c = conn.cursor()
#             if "nsfw_" in str(interaction.custom_id):
#                 print(f"preid: {interaction.custom_id}")
#                 iqid = str(interaction.custom_id).replace("nsfw_yes_", "")
#                 iqid = iqid.replace("nsfw_no_", "")
#                 print(f"postid: {iqid}")
#                 if "nsfw_yes_" in str(interaction.custom_id):
#                     command = f"update quotes set nsfw=True where qid={iqid}"
#                     c.execute(command)
#                 elif "nsfw_no_" in str(interaction.custom_id):
#                     command = f"update quotes set nsfw=False where qid={iqid}"
#                     c.execute(command)
#                 else:
#                     pass
#                 conn.commit()
#                 conn.close()
#             await interaction.message.delete()
#         except:
#             trace.print_exc()
#---------------------------------------------------------------------


    

    @quote.error
    async def arg_error_quote(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            msg = await ctx.send('Incorrect arguments entered | usage: **q!quote <@user/user#0000> <part-of-quote>**')
            await asyncio.sleep(10)
            await ctx.message.delete()
            await msg.delete()

    @qowote.error
    async def arg_error_qowote(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            msg = await ctx.send('Incorrect arguments entered | usage: **q!qowote <@user/user#0000> <part-of-quote>**')
            await asyncio.sleep(10)
            await ctx.message.delete()
            await msg.delete()

    @add.error
    async def arg_error_add(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            msg = await ctx.send('Incorrect arguments entered | usage: **q!add <@user/user#0000> <quote>**')
            await asyncio.sleep(10)
            await ctx.message.delete()
            await msg.delete()


    @delete.error
    async def arg_error_delete(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            msg = await ctx.send('Incorrect arguments entered | usage: **q!delete <@user/user#0000> <part-of-quote>**')
            await asyncio.sleep(10)
            await ctx.message.delete()
            await msg.delete()

    @profile.error
    async def arg_error_profile(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            msg = await ctx.send('Incorrect arguments entered | usage: **q!profile  <@user/user#0000>**')
            await asyncio.sleep(10)
            await ctx.message.delete()
            await msg.delete()


def setup(bot):
    bot.add_cog(Quotes(bot))
