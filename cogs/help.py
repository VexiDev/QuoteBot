import discord
from discord.errors import Forbidden
from discord.ext import commands 
import asyncio
import traceback as trace
import datetime
import random, string
from discord_components import *

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def rules(self, ctx):
    #     connect = self.bot.get_cog("Misc")
    #     # print('gotten connect')
    #     try:
    #         blist = await connect.checkblist(ctx, ctx.author)
    #     except:
    #         trace.print_exc()
    #     # print(f'connecting, {blist}')
    #     if blist is not None:
    #         if blist[1]=="global":
    #             # print('is global blist')
    #             await ctx.send(embed=blist[0])
    #             return
    #         else:
    #             pass
    #     else:
    #         pass
    #     rules = discord.Embed(title="QuoteBot Rules", description="Simple rules for a simple bot")
    #     rules.add_field(name=)

    @commands.command()
    async def help(self, ctx):
        if ctx.author.bot == True:
            return
        try:
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
            embedVar = discord.Embed(title="QuoteBot Help Menu", description="Store quotes quickly and easily", color=0x00ff00)
            embedVar.add_field(name="q!help", value="displays this message", inline=True)
            embedVar.add_field(name="q!invite", value="sends the invite link for Quotebot", inline=True)
            embedVar.add_field(name="q!info", value="displays general info on QuoteBot", inline=True)
            embedVar.add_field(name="q!add", value="usage: q!add <@user/user#000> <quote> \nAdds a quote to their stored quotes\n\n",inline=True)
            embedVar.add_field(name="q!delete", value="usage: q!delete <@user/user#000> <part-of-quote> \nRemoves a quote from a users stored quotes\n\n",inline=True)
            embedVar.add_field(name="q!profile", value="usage: q!profile <@user>\n Prints all quotes stored for set user\n\n",inline=True)
            embedVar.add_field(name="q!quote", value="usage: q!quote <@user/user#000> \nQuotes a random quote of a user\n",inline=True)
            embedVar.add_field(name="q!qowote", value="usage: q!qowote <@user/user#000> \nQuotes a random user but adds an uwu twist\n",inline=True)        
            embedVar.add_field(name="(**Requires Manage Server**)\nq!setquotechannel", value="usage: q!setquotechannel \n Sets the current  channel as the quote channel\nQuotebot commands will be locked to this channel\n\n", inline=True)
            embedVar.add_field(name="(**Requires Manage Server**)\nq!setlogger", value="usage: q!setlogger (**Requires Manage Server)**\n Sets the current channel as the log channel", inline=True)
            embedVar.add_field(name="q!request", value="usage: q!request <request>\nSends a message to me through Quotebot, this can be for support, to report abuse or to report bugs", inline=True)
            embedVar.add_field(name="q!setbio", value="usage: q!setbio <bio>\nAllows you to change your bio in q!profile", inline=True)
            embedVar.add_field(name="q!star", value="usage: q!star <part-of-quote>\nStars or UnStars a quote from your profile", inline=True)
            # embedVar.add_field(name="q!togglensfw", value="usage: q!togglensfw (optional: <user>, <force (true/false)>)\nToggles the ability to see nsfw content for a user or yourself. (Setting **force** to True means a user will not be able to enable nsfw content for themselves.)")
            embedVar.timestamp = datetime.datetime.utcnow()
            embedVar.set_footer(text=f"Developed by vexi#0420 | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            try:
                await ctx.author.send(embed=embedVar)
                msg = await ctx.send("Help has been sent!\n*check your dms*")
                await msg.add_reaction("😇")
                await asyncio.sleep(10)
                await msg.delete()
                await ctx.message.delete()
            except Forbidden:
                msg = await ctx.send('***I cannot dm you!***\nPlease unblock quotebot or enable dms from server members\nYou can also use q!qhelp to have help sent to this channel')
                await asyncio.sleep(10)
                await msg.delete()
                await ctx.message.delete()
        except:
            trace.print_exc()

    @commands.command()
    async def qhelp(self, ctx):
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
        embedVar = discord.Embed(title="QuoteBot Help Menu", description="Store quotes quickly and easily", color=0x00ff00)
        embedVar.add_field(name="q!help", value="displays this message", inline=True)
        embedVar.add_field(name="q!invite", value="sends the invite link for Quotebot", inline=True)
        embedVar.add_field(name="q!info", value="displays general info on QuoteBot", inline=True)
        embedVar.add_field(name="q!add", value="usage: q!add <@user/user#000> <quote> \nAdds a quote to their stored quotes\n\n",inline=True)
        embedVar.add_field(name="q!delete", value="usage: q!delete <@user/user#000> <part-of-quote> \nRemoves a quote from a users stored quotes\n\n",inline=True)
        embedVar.add_field(name="q!profile", value="usage: q!profile <@user>\n Prints all quotes stored for set user\n\n",inline=True)
        embedVar.add_field(name="q!quote", value="usage: q!quote <@user/user#000> \nQuotes a random quote of a user\n",inline=True)
        embedVar.add_field(name="q!qowote", value="usage: q!qowote <@user/user#000> \nQuotes a random user but adds an uwu twist\n",inline=True)        
        embedVar.add_field(name="(**Requires Manage Server**)\nq!setquotechannel", value="usage: q!setquotechannel \n Sets the current  channel as the quote channel\nQuotebot commands will be locked to this channel\n\n", inline=True)
        embedVar.add_field(name="(**Requires Manage Server**)\nq!setlogger", value="usage: q!setlogger (**Requires Manage Server)**\n Sets the current channel as the log channel", inline=True)
        embedVar.add_field(name="q!request", value="usage: q!request <request>\nSends a message to me through Quotebot, this can be for support, to report abuse or to report bugs", inline=True)
        embedVar.add_field(name="q!setbio", value="usage: q!setbio <bio>\nAllows you to change your bio in q!profile", inline=True)
        embedVar.add_field(name="q!star", value="usage: q!star <part-of-quote>\nStars or UnStars a quote from your profile", inline=True)
        # embedVar.add_field(name="q!togglensfw", value="usage: q!togglensfw (optional: <user>, <force (true/false)>)\nToggles the ability to see nsfw content for a user or yourself. (Setting **force** to True means a user will not be able to enable nsfw content for themselves.)")
        embedVar.timestamp = datetime.datetime.utcnow()
        embedVar.set_footer(text=f"Developed by vexi#0420 | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
        msg = await ctx.send(embed=embedVar)
        await asyncio.sleep(30)
        await msg.delete()
        await ctx.message.delete()

    @commands.command()
    async def review(self, ctx):
        if ctx.author.bot == True:
            return
        embed = discord.Embed(title="Quote Review Info", description="If your quote has been flagged for review Quotebot has detected either discriminatory or deragatory terms in your quote. You may also have attempted to add personal information such as Phone Numbers, Emails, Addresses or IPs to QuoteBot", color=0x00ff00)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(30)
        await msg.delete()
        await ctx.message.delete()

    @commands.command()
    async def blocked(self, ctx):
        if ctx.author.bot == True:
            return
        embed = discord.Embed(title="Quote Blocking Info:", description="Reasons your quote has been blocked by QuoteBot:", color=0x00ff00)
        embed.add_field(name="__Personal Information__:", value="If you quote contained any of the following it will be blocked from being added:\n- IPs\n- Phone Numbers\n- Email addresses\n- Addresses\n- SSN\n- Discord Token\nAttempting to add the information above will have your quote blocked and your attempt sent in for review by our team.")
        embed.add_field(name="__Links:__:", value="If your quote contained a link it will also be blocked. However, soon QuoteBot will support the adding of links and files to quotes to add context, store a file/image, or any other reason you would need to have a link or file on QuoteBot.")
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(30)
        await msg.delete()
        await ctx.message.delete()


    @commands.command()
    async def nsfw(self, ctx):
        if ctx.author.bot == True:
            return
        embed = discord.Embed(title="NSFW Quote Info", description="Quotebot does __not__ have strict rules on what can and can't be added, however we do seperate NSFW Quotes from normal ones. Quotes that are detected to contain homophobia, racism, sexism, etc. These quotes are stored in their own section of a users profile and cannot be added as a star quote", color=0x00ff00)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(30)
        await msg.delete()
        await ctx.message.delete()


    @commands.command()
    async def request(self, ctx, *, support=None):
        if ctx.author.bot == True:
            return
        try:
            connect = self.bot.get_cog("Misc")
            # print('gotten connect')
            try:
                blist = await connect.checkblist(ctx, ctx.author)
            except:
                trace.print_exc()
            # print(f'connecting, {blist}')
            if blist is not None:
                if blist[1]=="global" or blist[1]=="support":
                    # print('is global blist')
                    await ctx.send(embed=blist[0])
                    return
                else:
                    pass
            else:
                pass
            # global supportcount
            # print(supportcount)
            # print('supporting')
            guild = ctx.guild
            user = ctx.author
            # print('getting user')
            support_server = self.bot.get_guild(id=838814770537824378)
            dev = support_server.get_channel(918652907690287154)
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            print("Connected to database")
            c = conn.cursor()
            command = f"select * from users where uid={user.id}"
            print(command)
            c.execute(command)
            print("executed")
            results = c.fetchall()
            print(results)
            conn.commit()
            c.close()
            try:
                if results[0][5]==False:
                    await self.supportrun(ctx, guild, user, dev, support)
                elif results[0][5]==True:
                    check = await self.checktime(datetime.datetime.utcnow(), results[0][6], user)
                    if check==True:
                        await self.supportrun(ctx, guild, user, dev, support)
                    else:
                        print(f'request cooldown | uid:{ctx.author.id} | gid: {ctx.guild.id}')
                        # print(check.seconds/3600)
                        failed = discord.Embed(title="<:no:907768020561190983> Cooldown", description=f"You can only send one request per day!\n*You will be able to send another request in* **{check}h**", color=0xff0000)
                        await ctx.send(embed=failed)
                else:
                    print('request error, supportcooldown not True/False')
            except:
                trace.print_exc()
        except:
            trace.print_exc()

    async def checktime(self, timeA, timeB, user):
        try:
            # print(type(timeA))
            # print(type(timeB))
            days = timeA-timeB
            print(f'amount of days: {days.days}')
            if days.days>=1:
                connect = self.bot.get_cog("Misc")
                conn = connect.connectdb()
                print("Connected to database")
                c = conn.cursor()
                command = f"UPDATE users SET support_cooldown=False where uid={user.id}"
                print(command)
                c.execute(command)
                print("executed")
                conn.commit()
                c.close()
                return True
            else:
                return(24-((days.seconds)//3600))
        except:
            trace.print_exc()

    async def supportrun(self, ctx, guild, user, dev, support):
        
        try:
            if support == None:
                msg = await ctx.send("You must provide a detailed explanation of your issue. (Minimum of 50 characters)")
                await asyncio.sleep(4)
                await ctx.message.delete()
                await msg.delete()
            else:
                print(f'{len(support)}')
                if len(support) < 50:
                    msg = await ctx.send("You must provide a description that is longer then 50 characters")
                    await asyncio.sleep(4)
                    await ctx.message.delete()
                    await msg.delete()
                elif len(support) >= 2000:

                    msg=await ctx.send("Your description is too long (1000+ characters). To send this in please contact **vexi#0420** directly")
                    await asyncio.sleep(4)
                    await ctx.message.delete()
                    await msg.delete()
                                    
                else:
                    embed = discord.Embed(title="Your Request", description=f"-------\n{support}\n-------\n*You can only send* ***1*** *request per day*", color=0x00ff00)
                    confmsg = await ctx.send(content=f"Please confirm your request", embed=embed, components=[[Button(label="Send", style=3, custom_id=f"Confirm_Reply_{id}"),Button(label="Cancel", style=4, custom_id=f"Cancel_Reply_{id}")]])
                
                    print('confirming...')
                    # try:
                    def check(x):
                        return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id
                    response = await self.bot.wait_for("button_click", check=check)
                    # if response.custom_id==""
                    support_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                    print(f'adding request | ID: {support_id}')
                    # print('setting embed')
                    embed = discord.Embed(title=f"Request {support_id}", description=f'**Request:**\n {support}\n\n------------------------------------------------------------------------------------------', color=0x00ff00)
                    embed.add_field(name="Server Info:", value=f"**Name:** {ctx.guild.name}\n**ID:** {ctx.guild.id}\n**Members:** {len(ctx.guild.members)}", inline=True)
                    connect = self.bot.get_cog("Misc")
                    conn = connect.connectdb()
                    c = conn.cursor()
                    command = f"select quote from quotes where uid='{ctx.author.id}'"
                    print(command)
                    c.execute(command)
                    result = c.fetchall()
                    c.close()
                    embed.add_field(name="User Info:", value=f"**Name:** {ctx.author}\n**ID:** {ctx.author.id}\n**Quotes:** {len(result)}", inline=True)
                    # print('embed created')
                    embed.set_footer(text=f"QuoteBot | ID: {support_id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    # print('footer set')
                    embed.set_author(name=user, url=discord.Embed.Empty, icon_url=user.avatar_url)
                    # print('author set')
                    embed.timestamp = datetime.datetime.utcnow()
                    # print('set timestamp')
                    await dev.send(embed=embed)
                    # print('set')
                    #success = discord.Embed(title="Success <:yes:892537190347837450>", description="Your support request was successfully sent in!\n\n**Status:** *Open*\n**Comment:** *None*\n\nOnce your issue is resolved this message will update\n*You can only send one ticket every day*", color=0x00ff00)
                    success = discord.Embed(title="<:yes:892537190347837450> Success", description=f"Your request was successfully sent in!\n-------\n{support}\n-------\n\n**Status:** Open <:status_online:907767064926769242>\n**DevNote:** This message will update once I take action on your request\n\n*You can only send one request every day*", color=0x00ff00)
                    success.timestamp = datetime.datetime.utcnow()
                    success.set_footer(text=f"QuoteBot | ID: {support_id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    await confmsg.edit(content=f"<@{ctx.author.id}>",embed=success, components=[])
                    # await msg.pin(reason=f"Support Request ID:{support_id}")
                    connect = self.bot.get_cog("Misc")
                    conn = connect.connectdb()
                    print("Connected to database")
                    c = conn.cursor()
                    # print("cursored")
                    command = f"select * from support where sid='{support_id}'"
                    print(command)
                    c.execute(command)
                    result = c.fetchall()
                    if len(result)==0:
                        support = support.replace("'","''")
                        command = f"insert into support(sid, uid,gid,cid,mid,date_added,status,comment,request) values('{support_id}',{user.id},{guild.id},{ctx.channel.id},{confmsg.id},'{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}','open', 'none', '{support}')"
                        print(command)
                        c.execute(command)
                        print("executed")
                        command = f"UPDATE users SET support_cooldown=True where uid={user.id}"
                        print(command)
                        c.execute(command)
                        print("executed")
                        command = f"UPDATE users SET support_time='{datetime.datetime.utcnow()}' where uid={user.id}"
                        print(command)
                        c.execute(command)
                        print("executed")
                        conn.commit()
                        c.close()
                    else:
                        print('Duplicate ID for support request, retrying...')
                        await self.supportrun(ctx, guild, user, dev, support)
        except:
            trace.print_exc()

    @commands.command()
    async def reply(self, ctx, id, status,*, comment):
        if ctx.author.bot == True:
            return
        if ctx.author.id != 274213987514580993:
            return
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        print("Connected to database")
        c = conn.cursor()
        # print("cursored")
        command = f"select * from support where sid='{id}'"
        print(command)
        c.execute(command)
        result = c.fetchall()
        print(result)
        print("executed")
        try:
            try:
                channel = self.bot.get_channel(result[0][4])
                msg = await channel.fetch_message(result[0][5])
                support = result[0][9]
            except:
                print('\n')
                trace.print_exc()
                print('\n')
            if status.lower()=="complete":
                status="Complete <:status_online:907767064926769242>"
                newmsg = discord.Embed(title=f"<:complete:907780896722153573> Complete", description=f"Your request has been completed!\n-------\n{support}\n-------\n\n**Status:** {status}\n**DevNote:** {comment}\n\n*You can only send one request every day*", color=0x82ff47)
                newmsg.timestamp = datetime.datetime.utcnow()
                newmsg.set_footer(text=f"QuoteBot | ID: {id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            
            elif status.lower()=="deny":
                status="Denied <:dnd:907767435262828565>"
                newmsg = discord.Embed(title=f"<:Warning:909946407673274398> Denied", description=f"Your request has been denied!\n-------\n{support}\n-------\n\n**Status:** {status}\n**DevNote:** {comment}\n\n*You can only send one request every day*", color=0xff4f4f)
                newmsg.timestamp = datetime.datetime.utcnow()
                newmsg.set_footer(text=f"QuoteBot | ID: {id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            
            elif status.lower()=="wip":
                status="In-Progress <:status_idle:907767529139740722>"
                newmsg = discord.Embed(title=f"<:gears:907780900811583508> Updated", description=f"Your request has been updated!\n-------\n{support}\n-------\n\n**Status:** {status}\n**DevNote:** {comment}\n\n*You can only send one request every day*", color=0xffb521)
                newmsg.timestamp = datetime.datetime.utcnow()
                newmsg.set_footer(text=f"QuoteBot | ID: {id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            
            else:
                newmsg = discord.Embed(title=f"<:gears:907780900811583508> Updated", description=f"Your request has been updated!\n-------\n{support}\n-------\n\n**Status:** {status}\n**DevNote:** {comment}\n\n*You can only send one request every day*", color=0xffb521)
                newmsg.timestamp = datetime.datetime.utcnow()
                newmsg.set_footer(text=f"QuoteBot | ID: {id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")

            embed = discord.Embed(title=f'Update message of request: {id}', description=f"Status: {status}\nDevNote: {comment}", color=0x00ff00)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            nmsg = await ctx.send(content="Please confirm your reply",embed=embed, components=[[Button(label="Send", style=3, custom_id=f"Confirm_Reply_{id}"),Button(label="Cancel", style=4, custom_id=f"Cancel_Reply_{id}")]])
            print('confirming...')
        except:
            trace.print_exc()
        # try:
        def check(x):
            return x.author.id == ctx.author.id and x.guild.id == ctx.guild.id and x.channel.id == ctx.channel.id
        response = await self.bot.wait_for("button_click", check=check)
        print(response.custom_id)
        if response.custom_id == f"Confirm_Reply_{id}":
            print("Confirmed")
            await msg.edit(content=f"<:member_join:908033530901192734> {msg.content}",embed=newmsg, components=[])
            await channel.send(f'<@{result[0][2]}>, Your request from **{result[0][6].strftime("%d/%m/%Y")}** has been updated!\n*the message has been pinned*')
            await msg.pin(reason=f"Request Updated - ID:{id}")
            print('updating databse')
            status = status.replace("'","''")
            command = f"UPDATE support SET status='{status}' where sid='{id}'"
            print(command)
            c.execute(command)
            comment = comment.replace("'","''")
            command = f"Update support set comment='{comment}' where sid='{id}'"
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            embed = discord.Embed(title=f'<:yes:892537190347837450> Successfully updated message of request: {id}', description=f"Status: {status}\nDevNote: {comment}", color=0x00ff00)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"QuoteBot | ID: {ctx.author.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
            await nmsg.edit(content="",embed=embed, components=[])
        elif response.custom_id == f"Cancel_Reply_{id}":
            print("Canceled")
            embed = discord.Embed(title="<:no:907768020561190983> Canceled", color=0xff0000)
            await nmsg.edit(content="",embed=embed, components=[])
            return

        
    @commands.command()
    async def addusers(self, ctx):
        if ctx.author.bot == True:
            return
        if ctx.author.id != 274213987514580993:
            return
        connect = self.bot.get_cog("Misc")
        conn = connect.connectdb()
        print("Connected to database")
        c = conn.cursor()
        # print("cursored")
        try:
            for guild in self.bot.guilds:
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
                        command = f"insert into users(uid, nsfw, global_blist, support_blist,support_cooldown, support_time, blist_reason, bio) values({user.id}, True, False, False, False, '{date}', 'None', 'None')"
                        # print(command)
                        c.execute(command)
                        # print("executed")
                        print('added user\n----------')
                    else:
                        print("duplicate user or bot\n----------")
                    #e
        except:
            trace.print_exc()
        conn.commit()
        c.close()



                

def setup(bot):
    bot.add_cog(Help(bot))
