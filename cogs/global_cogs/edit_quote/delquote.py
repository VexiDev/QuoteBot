import discord
import datetime
import traceback
import asyncio
from discord import app_commands
from discord.ext import commands

class delquote(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def delete(self, interaction: discord.Interaction, user: discord.User):
        #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
        #Send loading message
        await interaction.response.defer()
        #assign message for future edits
        message = await interaction.followup.send(embed=loading_embed)

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

        #check user blacklist
        status = await action_manager.user_blacklist_actions(interaction, message, database)
        if status == "user_blacklisted":
            return
        #check target blacklist
        status = await action_manager.target_blacklist_actions(interaction, user, message, database)
        if status == "target_blacklisted":
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

        #-----CHECK FOR EXIST-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non hidden quotes that contain the input
        command = f"select * from quotes where uid={user.id} and guild_id={interaction.guild.id} and hidden=False"
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
            no_quote_embed = discord.Embed(title=f"{user.display_name} has no quotes", description="-\nAdd some with **/add**", color=0xe02f2f)
            #Create fake quote author for confirm
            no_quote_embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            no_quote_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            no_quote_embed.timestamp = datetime.datetime.utcnow()

            await interaction.followup.send(embed=no_quote_embed, ephemeral=True)
            await message.delete()
            return

        #if there is more then 1 quote, the filter term was too common
        else:
            select_options = []
                
            #SEND FILTER TOO COMMON EMBED
            select_quote_embed = discord.Embed(title="Select a quote", description=f"Please select the quote you want to delete from QuoteBot", color=0xe02f2f)
            #Create fake quote author for confirm
            select_quote_embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            select_quote_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            select_quote_embed.timestamp = datetime.datetime.utcnow()

            for quote in results:
                if len(quote[3]) == 10:
                    quote_date = datetime.datetime.strptime(quote[3], "%d/%m/%Y").strftime("%d/%m/%Y")
                elif len(quote[3]) == 19:
                    quote_date = datetime.datetime.strptime(quote[3], "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
                else:
                    quote_ddate = ""
                select_options.append(discord.SelectOption(label=f"{quote[2][:97]}{'...' if len(quote[2]) > 97 else ''}", description=f"Added on {quote_date}", value=f"{quote[0]}"))

            # Split select_options into sublists of 25 or less
            select_options = [select_options[i:i+25] for i in range(0, len(select_options), 25)]

            selected_quote = await self.update_delete_dropdown(interaction, select_quote_embed, select_options, 0, message)

        if selected_quote == None or selected_quote == "qb-cancel-command-c2vzOQ":
            try:
                await message.delete()
            except:
                #if it failed prob got canceled so we ignore
                pass

            return

        delete_quote = [result for result in results if str(result[0]) == str(selected_quote)][0]

        verify_embed = discord.Embed(title=f"\n\"{delete_quote[2]}\"\n", description=f"-\n*Please confirm that the quote above is correct*", color=0xff6161)
        #Create fake quote author for confirm
        verify_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
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

            #check if any quote channel is set
            command = f"select * from channels where guild_id={interaction.guild.id} and type='quotes'"
            #execute command
            c.execute(command)
            #get results
            channels = c.fetchall()
            #close database connection
            c.close()
            conn.close()
            

            if len(channels) != 0:
                quote_channel = await interaction.guild.fetch_channel(int(channels[0][2]))
                original_quote_msg = quote_channel.get_partial_message(int(results[0][8]))
                try:
                    await original_quote_msg.delete()
                except:
                    for text_channel in interaction.guild.text_channels:
                    #get original quote message
                        try:
                            quote_channel = await interaction.guild.fetch_channel(text_channel.id)
                            new_found_quote = quote_channel.get_partial_message(int(results[0][8]))
                            final_quote = await new_found_quote.fetch()
                            if final_quote.id == results[0][8]:
                                print(" vv |DELQUOTE TEMP DEBUG| vv")
                                print("original: ", results[0][8],"\nfound: ",final_quote.id)
                                await new_found_quote.delete()
                                break
                            else:
                                pass
                        except:
                            pass

            elif len(channels) == 0:
                for text_channel in interaction.guild.text_channels:
                    #get original quote message
                    try:
                        original_quote_msg = text_channel.get_partial_message(int(results[0][8]))
                        await original_quote_msg.delete()
                        break
                    except:
                        pass

            complete_embed = discord.Embed(title=f"Quote Deleted",description=f"\"{delete_quote[2]}\"", color=0xff6161)
            #Add user as author
            complete_embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            complete_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            complete_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=complete_embed, view=None)
            
        else:
            #create canceled embed
            canceled_embed = discord.Embed(description="<:no:907768020561190983> **Canceled**",  color=0xff0000)
                        
            await interaction.followup.send(embed=canceled_embed, ephemeral=True)
            await message.delete()
            return

    async def update_delete_dropdown(self, interaction, select_quote_embed, select_options, page, message):
        dropdown = self.quote_delete_dropdown(select_options, page)
        await message.edit(embed=select_quote_embed, view=dropdown)
        await dropdown.wait()
        if dropdown.done == False:
            if dropdown.cancel is True:
                #create canceled embed
                canceled_embed = discord.Embed(description="<:no:907768020561190983> **Canceled**",  color=0xff0000)
                await interaction.followup.send(embed=canceled_embed, ephemeral=True)
                await message.delete()
                return 'qb-cancel-command-c2vzOQ'
            
            elif dropdown.selection == 'next':
                page += 1
                await self.update_delete_dropdown(interaction, select_quote_embed, select_options, page, message)
            
            elif dropdown.selection == 'back':
                page -= 1
                await self.update_delete_dropdown(interaction, select_quote_embed, select_options, page, message)
        
        else:
            return dropdown.selection 

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

    class timed_out(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @discord.ui.button(label='This message has timed out', style=discord.ButtonStyle.grey, disabled=True)
        async def timeout(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.value = False
            self.stop()

    class quote_delete_dropdown(discord.ui.View):
        def __init__(self, select_options, page, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.cancel = False
            self.page = page
            self.done = False
            self.select_options = select_options

            self.select = discord.ui.Select(placeholder="Select the quote you wish to delete", options=select_options[self.page], min_values=1, max_values=1, row=1)
            self.select.callback = self.quote_dropdown
            self.add_item(self.select)

            self.back_button = discord.ui.Button(label='Back', style=discord.ButtonStyle.blurple, emoji="<:previous:1014353821968896080>", row=2)
            self.back_button.callback = self.back_page
            if self.page == 0:
                self.back_button.disabled = True
            self.add_item(self.back_button)

            self.next_button = discord.ui.Button(label='Next', style=discord.ButtonStyle.blurple, emoji="<:next:1014353798203985930> ", row=2)
            self.next_button.callback = self.next_page
            if self.page == len(select_options)-1:
                self.next_button.disabled = True
            self.add_item(self.next_button)


            self.cancel_button = discord.ui.Button(label='Cancel', style=discord.ButtonStyle.red, row=2)
            self.cancel_button.callback = self.cancel_delete
            self.add_item(self.cancel_button)

        async def quote_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = interaction.data['values'][0] if interaction.data['values'][0] else None
            self.done = True
            self.stop()

        async def next_page(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = 'next'
            self.stop()

        async def back_page(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = 'back'
            self.stop()

        async def cancel_delete(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.cancel = True
            self.stop()
                
                


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(delquote(bot), guilds = commands.Greedy[discord.Object])
