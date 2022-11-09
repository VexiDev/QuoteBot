import discord
import datetime
import traceback
import asyncio
from discord import app_commands
from discord.ext import commands

class delquote(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def delete(self, interaction: discord.Interaction, user: discord.User, quote=""):
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
        #import system checks cog
        action_manager = self.bot.get_cog("action_manager")
        profile_manager = self.bot.get_cog("profile_creator")
        #check maintenance
        #check channel restrictions
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
        
        #----Replace single quotes-----
        quote = quote.replace("'", "''")

        #-----CHECK FOR EXIST-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select * from quotes where uid={user.id} and guild_id={interaction.guild.id} and lower(quote) like lower('%{quote}%') and hidden=False"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        #if nothing in results, no matching quote was found
        if len(results) == 0:
            #SEND NO QUOTE FOUND EMBED
            no_quote_embed = discord.Embed(title="No quote was found", description="Make sure you've spelled everything correctly", color=0xe02f2f)
            #Create fake quote author for confirm
            no_quote_embed.set_author(name=user, icon_url=user.display_avatar.url)
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
        elif len(results) > 1:
            #SEND FILTER TOO COMMON EMBED
            bad_filter_embed = discord.Embed(title="Filter term too common", description=f"I found {len(results)} quotes that include:\n**\"{quote}\"**\n-\nPlease add more of the quote you wish to remove", color=0xe02f2f)
            #Create fake quote author for confirm
            bad_filter_embed.set_author(name=user, icon_url=user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            bad_filter_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            bad_filter_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=bad_filter_embed)

            #wait 5 seconds for message reading
            await asyncio.sleep(5)
            try:
                #after timeout delete the message
                await message.delete()
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

        delete_quote = results[0]
        verify_embed = discord.Embed(title=f"\n\"{delete_quote[2]}\"\n", description=f"-\n*Please confirm that the quote above is correct*", color=0xff6161)
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
            confirm_embed = discord.Embed(title="Please wait while we delete the quote", description="<a:loading:892534287415525386> Processing request", color=0x068acc)
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
            #create query to add quote to user database
            command = f"update quotes set hidden=true where qid={delete_quote[0]}"
            #execute command
            c.execute(command)
            #commit changes
            conn.commit()
            #close database connection
            c.close()
            conn.close()

            #check if any quote channel is set
             #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            #create query to add quote to user database
            command = f"select * from channels where guild_id={interaction.guild.id} and type='quotes'"
            #execute command
            c.execute(command)
            #get results
            channels = c.fetchall()
            #close database connection
            c.close()
            conn.close()
            

            try:
                if len(channels) != 0:
                    quote_channel = await interaction.guild.fetch_channel(int(channels[0][2]))
                    print(quote_channel)
                    original_quote_msg = quote_channel.get_partial_message(int(results[0][8]))
                    await original_quote_msg.delete()


                elif len(channels) == 0:
                    for text_channel in interaction.guild.text_channels:
                        #get original quote message
                        try:
                            original_quote_msg = text_channel.get_partial_message(int(results[0][8]))
                        except:
                            pass
                        await original_quote_msg.delete()
                
            except:
                try:
                    for text_channel in interaction.guild.text_channels:
                            #get original quote message
                            try:
                                original_quote_msg = text_channel.get_partial_message(int(results[0][8]))
                            except:
                                pass
                            await original_quote_msg.delete()
                except:
                    traceback.print_exc()

            complete_embed = discord.Embed(title=f"Quote Deleted",description=f"\"{delete_quote[2]}\"", color=0xff6161)
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
    await bot.add_cog(delquote(bot), guilds = commands.Greedy[discord.Object])
