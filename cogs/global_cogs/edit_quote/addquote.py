import discord
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands

class addquote(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def add(self, interaction: discord.Interaction, user: discord.User, quote=""):
        #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
        #Send loading message
        await interaction.response.send_message(embed=loading_embed)
        #assign message for future edits
        message = await interaction.original_response()

        #set database variable
        database = self.bot.get_cog("database")

        #------Pass System Checks-----
        #import system check cogs
        content_filter = self.bot.get_cog("content_filter")
        action_manager = self.bot.get_cog("action_manager")
        profile_manager = self.bot.get_cog("profile_creator")
        #check maintenance

        #check for quote channel
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select * from channels where guild_id={interaction.guild.id} and type='quotes'"
        #execute command
        c.execute(command)
        #get results of query
        channel=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        #check if profile exist for both user and target
        await profile_manager.creator(interaction.user)
        await profile_manager.creator(user)

        #check blacklist
        status = await action_manager.blacklist_actions(interaction, message, database)
        if status == "blacklisted":
            return

        #check if user is a bot
        if user.bot or interaction.user.bot:
            #if is a bot cancel request
            is_bot_embed = discord.Embed(title="Bots cannot use QuoteBot", color=0xe02f2f)
            await message.edit(embed=is_bot_embed)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass


        #check content filter
        #default nsfw to false
        nsfw = False
        #send quote to filter api
        filter_result = await content_filter.check_nsfw(quote)
        #take action based on results
        nsfw = await action_manager.nsfw_actions(interaction, message, user, nsfw, quote, filter_result)
        #if action manager blocks the quote end add function
        if nsfw == "blocked":
            return

        #----Replace single quotes-----
        #save original quote for final message
        msg_quote = quote
        quote = quote.replace("'", "''")

        #-----CHECK FOR DUPLICATE-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select * from quotes where uid={user.id} and guild_id={interaction.guild.id} and lower(quote) like lower('{quote}')"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        #if anything in results, a duplicate was found
        if len(results) != 0:
            duplicate_embed = discord.Embed(title=f"Quote Already Exists", description=f"The following quote is already in your server profile:\n\"{msg_quote}\"", color=0xDF3B57)
            duplicate_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            duplicate_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=duplicate_embed)
            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass
        if nsfw:
            verify_embed = discord.Embed(title=f"\n\"{msg_quote}\"\n", description=f"-\n<:alert2:1016826438718066790> **This quote has been flagged and will be placed in the NSFW category**\n-\n*Please confirm that the quote above is correct*", color=0x42f56f)
        else:
            verify_embed = discord.Embed(title=f"\n\"{msg_quote}\"\n", description=f"-\n*Please confirm that the quote above is correct*", color=0x42f56f)

        #Create fake quote author for confirm
        verify_embed.set_author(name=user, icon_url=user.display_avatar.url)
        #CREATE PAGE FOOTER
        #create footer with USERID
        verify_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        #set timestamp to discord time
        verify_embed.timestamp = datetime.datetime.utcnow()
        confirm_buttons = self.Confirm()
        await message.edit(embed=verify_embed, view=confirm_buttons)

        await confirm_buttons.wait()
        if confirm_buttons.value is None:
            #if timed out delete message
            await message.delete()
            #if timed out place warning in console
            print(f'WARNING: confirm_buttons() view in server {interaction.guild.id} has timed out')
        elif confirm_buttons.value:
            confirm_embed = discord.Embed(title="Please wait while we add your quote", description="<a:loading:892534287415525386> Processing request", color=0x068acc)
            #CREATE PAGE FOOTER
            #create footer with USERID
            confirm_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            confirm_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=confirm_embed, view=None)
            
            #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            #get message id of original interaction
            msg = await message.fetch()
            #create query to add quote to user database
            command = f"insert into quotes(uid, quote, date_added, guild_id, nsfw, star, added_by, message) values({user.id}, '{quote}','{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}',{interaction.guild.id},{nsfw},False, {interaction.user.id}, {msg.id})"
            #execute command
            c.execute(command)
            #commit changes
            conn.commit()
            #close database connection
            c.close()
            conn.close()

            if len(channel) == 1:

                msg_channel = await self.bot.fetch_channel(channel[0][2])
                complete_embed = discord.Embed(title=f"\"{msg_quote}\"", color=0x00ff2f)
                #Add user as author
                complete_embed.set_author(name=user, icon_url=user.display_avatar.url)
                #CREATE PAGE FOOTER
                #create footer with USERID
                complete_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                complete_embed.timestamp = datetime.datetime.utcnow()
                await msg_channel.send(embed=complete_embed)
                msg_complete_embed = discord.Embed(title=f"Your quote has been successfully added",description=f"It has been sent in <#{msg_channel.id}>", color=0x00ff2f)
                #Add user as author
                msg_complete_embed.set_author(name=user, icon_url=user.display_avatar.url)
                #CREATE PAGE FOOTER
                #create footer with USERID
                msg_complete_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                msg_complete_embed.timestamp = datetime.datetime.utcnow()
                await message.edit(embed=msg_complete_embed, view=None)

            elif len(channel) > 1:
                channel_error_embed = discord.Embed(title=f"A channel error has occured",description=f"Please set your quotes channel again using **/setchannel** then try again\n*We apologize for the inconvenience*", color=0xDF3B57)
                channel_error_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                channel_error_embed.timestamp = datetime.datetime.utcnow()
                await message.edit(embed=channel_error_embed)
                try:
                    #after timeout delete the message
                    await message.delete(delay=5)
                    return
                except:
                    #if it fails means it was hidden therefore we ignore
                    pass
            else:
                complete_embed = discord.Embed(title=f"\"{msg_quote}\"", color=0x00ff2f)
                #Add user as author
                complete_embed.set_author(name=user, icon_url=user.display_avatar.url)
                #CREATE PAGE FOOTER
                #create footer with USERID
                complete_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                complete_embed.timestamp = datetime.datetime.utcnow()
                await message.edit(embed=complete_embed, view=None)
            
        else:
            #create canceled embed
            canceled_embed = discord.Embed(description="<:no:907768020561190983> **Canceled**",  color=0xff0000)
            await message.edit(embed=canceled_embed, view=None)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass


    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None


        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji="<:yes:892537190347837450>")
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.value = True
            self.stop()

        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji="<:no:907768020561190983>")
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.value = False
            self.stop()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(addquote(bot), guilds = commands.Greedy[discord.Object])
