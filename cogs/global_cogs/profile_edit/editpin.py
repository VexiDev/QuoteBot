import discord
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands

class edit_pin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def pin(self, interaction: discord.Interaction, quote="", hidden=False):
        #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
        #Send loading message
        await interaction.response.send_message(embed=loading_embed, ephemeral=hidden)
        #assign message for future edits
        message = await interaction.original_response()

        #set database variable
        database = self.bot.get_cog("database")

        #------Pass System Checks-----
        #import system checks cog
        action_manager = self.bot.get_cog("action_manager")
        profile_manager = self.bot.get_cog("profile_creator")
        #check maintenance
        #check channel restrictions
        #check if profile exist for user 
        await profile_manager.creator(interaction.user)
        #check blacklist
        status = await action_manager.blacklist_actions(interaction, message, database)
        if status == "blacklisted":
            return
        #check if user is a bot
        if interaction.user.bot:
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
        
        #----Replace single quotes-----
        quote = quote.replace("'", "''")

        #-----CHECK FOR EXIST-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query to find the quote in user base
        command = f"select distinct * from quotes where uid={interaction.user.id} and lower(quote) like lower('%{quote}%')"
        #execute command
        c.execute(command)
        #get results of query
        pinquote=c.fetchall()
        #create query to get all star quotes
        command = f"select * from quotes where uid={interaction.user.id} and star=True"
        #execute command
        c.execute(command)
        #get results of query
        starquote=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        #if nothing in results, no matching quote was found
        if len(pinquote) == 0:
            #SEND NO QUOTE FOUND EMBED
            no_quote_embed = discord.Embed(title="No matching quote was found", description=f"I looked for quotes like:\n\"{quote}\"\n-\nMake sure you've spelled everything correctly", color=0xe02f2f)
            #Create fake quote author for confirm
            no_quote_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            no_quote_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            no_quote_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=no_quote_embed)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

        #if there is more then 1 quote, the filter term was too common
        elif len(pinquote) > 1:
            #check if the quotes are duplicates
            for q in range(len(pinquote)-1):
                # if they arent send error message else just pick the first one
                if pinquote[q][2] != pinquote[q+1][2]:
                    #SEND FILTER TOO COMMON EMBED
                    bad_filter_embed = discord.Embed(title="Your quote was too common", description=f"I found {len(pinquote)} quotes that include:\n**\"{quote}\"**\n-\nPlease add more of the quote you wish to pin", color=0xe02f2f)
                    #Create fake quote author for confirm
                    bad_filter_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                    #CREATE PAGE FOOTER
                    #create footer with USERID
                    bad_filter_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                    #set timestamp to discord time
                    bad_filter_embed.timestamp = datetime.datetime.utcnow()
                    await message.edit(embed=bad_filter_embed)
                    break

                    try:
                        #after timeout delete the message
                        await message.delete(delay=5)
                        return
                    except:
                        #if it fails means it was hidden therefore we ignore
                        pass

        #if there is only 1 quote  check if its the same one
        elif len(pinquote) == 1 and len(starquote) == 1:
            
            if pinquote[0][0] == starquote[0][0]:
                #SEND FILTER TOO COMMON EMBED
                duplicate_embed = discord.Embed(title="This is already your pinned quote", color=0xffb300)
                #Create fake quote author for confirm
                duplicate_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                #CREATE PAGE FOOTER
                #create footer with USERID
                duplicate_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                duplicate_embed.timestamp = datetime.datetime.utcnow()
                await message.edit(embed=duplicate_embed)

                try:
                    #after timeout delete the message
                    await message.delete(delay=5)
                    return
                except:
                    #if it fails means it was hidden therefore we ignore
                    pass

        elif pinquote[0][5] == True:
            #SEND NO NSFW EMBED
            nsfw_embed = discord.Embed(title="NSFW quotes cannot be pinned",description="Look in your profile for a non nsfw quote", color=0xe02f2f)
            #Create fake quote author for confirm
            nsfw_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            nsfw_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            nsfw_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=nsfw_embed)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

        pinned_quote = pinquote[0]
        verify_embed = discord.Embed(title=f"\n\"{pinned_quote[2]}\"\n", description=f"-\n*Please confirm that the quote above is correct*", color=0xffb300)
        #Create fake quote author for confirm
        verify_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
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
            confirm_embed = discord.Embed(title="Please wait while we pin your quote", description="<a:loading:892534287415525386> Processing request", color=0x068acc)
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
            #check if any pre existing quotes
            if len(starquote) == 0:
                #create query to add quote to user database
                command = f"update quotes set star=True where uid={interaction.user.id} and qid={pinned_quote[0]}"
            
            else:
                #create loop to get remove all current star quote and then pin the current one
                for star in starquote:
                    #create query to remove star quote
                    command = f"update quotes set star=False where uid={interaction.user.id} and qid={star[0]}"
                    #execute command
                    c.execute(command)

                #create query to pin the current quote
                command = f"update quotes set star=True where uid={interaction.user.id} and qid={pinned_quote[0]}"
            #execute command
            c.execute(command)
            #commit all changes
            conn.commit()
            #close database connection
            c.close()
            conn.close()

            #send complete message
            complete_embed = discord.Embed(description=f"<:pinned:1014361955995230288> **\"{pinned_quote[2]}\"**\n-\n*This quote is now visible on your profile home page*", color=0xffb300)
            #Add user as author
            complete_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            complete_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            complete_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=complete_embed, view=None)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

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
    await bot.add_cog(edit_pin(bot), guilds = commands.Greedy[discord.Object])
