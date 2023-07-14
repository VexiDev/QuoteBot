import discord
import datetime
import traceback
from discord import app_commands
from discord.ext import commands

class user_lookup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def user_lookup(self, interaction: discord.Interaction, user: discord.User, hidden=False):
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
        #check if profile exist for both user and target
        await profile_manager.creator(interaction.user)
        await profile_manager.creator(user)
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

        #-----GET PROFILE INFO-----
        #get user bio
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select bio from users where uid={user.id}"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()
        if results[0][0] != "None":
            bio = results[0][0]
        else:
            bio = "\u200B"

        #get user pinned quote
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select quote from quotes where uid={user.id} and star=True"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()
        if len(results) != 0:
            pin = f"\"{results[0][0]}\""
            pintag = f"ㅤㅤ-{user.name}"
        else:
            pin = "Pin a quote with **/pin**"
            pintag = "\u200B"

        #-----GET NORMAL USER QUOTES-----
        #get database credentials from database cog
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select * from quotes where uid={user.id} and nsfw=False and hidden=False"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        normal_count = len(results)
        #close database connection
        c.close()
        conn.close()
        #check if any quotes were found
        if len(results) != 0:
            #create empty list to store all quote strings
            only_quotes = []
            #iterate through results storing only quote strings
            for quotes in results:
                only_quotes.append((quotes[2],quotes[3]))
            #seperate quotes into lists of 10 (or a single list if <=10)
            if len(only_quotes) > 9:
                only_quote_pages = [only_quotes[i:i + 9] for i in range(0, len(only_quotes), 9)]
            #if no quotes were found set no quote page (to be implemented)
            elif len(only_quotes) == 0:
                pass
            else:
                #if there are less then 10 quotes simply create a single page of those quotes
                only_quote_pages = [only_quotes]
            #create empty page for pagination of quotes
            normal_quote_pages = []
            #create page counter variable
            page_count = 1
            #iterate through pages converting them to embeds
            for page in only_quote_pages:
                embed_page = discord.Embed(title=f"{user.display_name}'s Quotes (Page {page_count}/{len(only_quote_pages)})", description=f"Server: {interaction.guild.name}", color=0x8AEA92)
                #create footer with USERID
                embed_page.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                embed_page.timestamp = datetime.datetime.utcnow()
                for quote in page:
                    if len(quote[1]) == 10:
                        quote_date = datetime.datetime.strptime(quote[1], "%d/%m/%Y").strftime("%d/%m/%Y")
                    elif len(quote[1]) == 19:
                        quote_date = datetime.datetime.strptime(quote[1], "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
                    else:
                        quote_date = "legacy quote"
                    embed_page.add_field(name=f"\"{quote[0]}\"", value=f"\- *{quote_date}*")
                normal_quote_pages.append(embed_page)
                page_count += 1
        #if no quotes are found create a no quote page
        else:
            embed_page = discord.Embed(title=f"{user} has no quotes", description=f"-\nAdd some with **/add**!\n\u200B", color=0xDF3B57)
            #create footer with USERID
            embed_page.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            embed_page.timestamp = datetime.datetime.utcnow()
            normal_quote_pages = [embed_page]

        #-----GET NSFW USER QUOTES-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all  nsfw quotes
        command = f"select * from quotes where uid={user.id} and nsfw=True and hidden=False"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        nsfw_count=len(results)
        #close database connection
        c.close()
        conn.close()
        #check if any nsfw quotes were found
        if len(results) != 0:
            #create empty list to store all quote strings
            only_quotes = []
            #iterate through results storing only quote strings
            for quotes in results:
                only_quotes.append((quotes[2],quotes[3]))
            #seperate quotes into lists of 10 (or a single list if <=10)
            if len(only_quotes) > 9:
                only_quote_pages = [only_quotes[i:i + 9] for i in range(0, len(only_quotes), 9)]
            #if no quotes were found set no quote page (to be implemented)
            elif len(only_quotes) == 0:
                pass
            else:
                #if there are less then 10 quotes simply create a single page of those quotes
                only_quote_pages = [only_quotes]
            #create empty page for pagination of quotes
            nsfw_quote_pages = []
            #create page counter variable
            page_count = 1
            #iterate through pages converting them to embeds
            for page in only_quote_pages:
                embed_page = discord.Embed(title=f"{user.display_name}'s NSFW Quotes (Page {page_count}/{len(only_quote_pages)})", description=f"Server: {interaction.guild.name}", color=0xDF3B57)
                #create footer with USERID
                embed_page.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                embed_page.timestamp = datetime.datetime.utcnow()
                for quote in page:
                    if len(quote[1]) == 10:
                        quote_date = datetime.datetime.strptime(quote[1], "%d/%m/%Y").strftime("%d/%m/%Y")
                    elif len(quote[1]) == 19:
                        quote_date = datetime.datetime.strptime(quote[1], "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
                    else:
                        pass
                    embed_page.add_field(name=f"\"{quote[0]}\"", value=f"\- *{quote_date}*")
                nsfw_quote_pages.append(embed_page)
                page_count += 1
        
        #if no nsfw quotes found create no quote page
        else:
            embed_page = discord.Embed(title=f"{user} has no NSFW Quotes", description=f"-\nIf Quotebot or our team detect one it will be placed here\n\u200B", color=0xDF3B57)
            #create footer with USERID
            embed_page.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            embed_page.timestamp = datetime.datetime.utcnow()
            nsfw_quote_pages = [embed_page]
            
        #-----GET DELETED USER QUOTES-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all  nsfw quotes
        command = f"select * from quotes where uid={user.id} and hidden=True"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        hidden_count=len(results)
        #close database connection
        c.close()
        conn.close()
        #check if any nsfw quotes were found
        if len(results) != 0:
            #create empty list to store all quote strings
            only_quotes = []
            #iterate through results storing only quote strings
            for quotes in results:
                only_quotes.append((quotes[2],quotes[3]))
            #seperate quotes into lists of 10 (or a single list if <=10)
            if len(only_quotes) > 9:
                only_quote_pages = [only_quotes[i:i + 9] for i in range(0, len(only_quotes), 9)]
            #if no quotes were found set no quote page (to be implemented)
            elif len(only_quotes) == 0:
                pass
            else:
                #if there are less then 10 quotes simply create a single page of those quotes
                only_quote_pages = [only_quotes]
            #create empty page for pagination of quotes
            hidden_quote_pages = []
            #create page counter variable
            page_count = 1
            #iterate through pages converting them to embeds
            for page in only_quote_pages:
                embed_page = discord.Embed(title=f"{user}'s Deleted Quotes (Page {page_count}/{len(only_quote_pages)})", description=f"Server: **Global User Lookup**", color=0xDF3B57)
                #create footer with USERID
                embed_page.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                embed_page.timestamp = datetime.datetime.utcnow()
                for quote in page:
                    if len(quote[1]) == 10:
                        quote_date = datetime.datetime.strptime(quote[1], "%d/%m/%Y").strftime("%d/%m/%Y")
                    elif len(quote[1]) == 19:
                        quote_date = datetime.datetime.strptime(quote[1], "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
                    else:
                        quote_date = "legacy quote"
                    embed_page.add_field(name=f"\"{quote[0]}\"", value=f"\- *{quote_date}*")
                hidden_quote_pages.append(embed_page)
                page_count += 1
        
        #if no nsfw quotes found create no quote page
        else:
            embed_page = discord.Embed(title=f"{user} has no Deleted Quotes", description=f"-\nIf a quote gets deleted it will be viewable here\n\u200B", color=0xDF3B57)
            #create footer with USERID
            embed_page.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            embed_page.timestamp = datetime.datetime.utcnow()
            hidden_quote_pages = [embed_page]

        #-----CREATE PROFILE MAIN PAGE-----

        #CREATE MAIN PAGE
        account_age = (user.created_at).strftime("%d/%m/%Y")
        #Create embed home page embed, if user bio is not None set description to the bio
        if bio != "\u200B":
            profile_home_page = discord.Embed(title=f"User Lookup: {user.id}", description=f"-\nName: {user}\nAccount Age: {account_age}\nTotal Quotes: {normal_count+nsfw_count}\nNormal Quotes: {normal_count}\nNSFW Quotes: {nsfw_count}\nDeleted Quotes: {hidden_count}\n\n-\n{bio}\n-", color=0x54de99)
        else:
            profile_home_page = discord.Embed(title=f"User Lookup: {user.id}", description=f"-\nName: {user}\nAccount Age: {account_age}\nTotal Quotes: {normal_count+nsfw_count}\nNormal Quotes: {normal_count}\nNSFW Quotes: {nsfw_count}\nDeleted Quotes: {hidden_count}\n\n-", color=0x54de99)

        #set page thumbnail to user's SERVER profile
        profile_home_page.set_thumbnail(url=user.display_avatar.url)
        #add a field for pinned quote
        profile_home_page.add_field(name=f"<:pinned:1014361955995230288> {pin}", value=f"{pintag}")
        
        #CREATE PAGE FOOTER
        #create footer with USERID
        profile_home_page.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        #set timestamp to discord time
        profile_home_page.timestamp = datetime.datetime.utcnow()

        #call for profile page response
        await self.profile_page(interaction, hidden, message, profile_home_page, normal_quote_pages, nsfw_quote_pages, hidden_quote_pages)

    #seperate profile page menu into function
    async def profile_page(self, interaction, hidden, message, profile_home_page, normal_quote_pages, nsfw_quote_pages, hidden_quote_pages):
        #-----SEND PAGE-----
        #set pageselect view to variable for wait
        home_page_buttons = self.HomePageSelect()
        #send profile home page, set to ephemeral if hidden is True
        await message.edit(embed=profile_home_page, view=home_page_buttons)
        #wait for buttons to stop waiting for response
        await home_page_buttons.wait()
        await self.profile_menu_pages(interaction, hidden, message, home_page_buttons, profile_home_page, normal_quote_pages, nsfw_quote_pages, hidden_quote_pages)

    async def profile_menu_pages(self, interaction, hidden, message, home_page_buttons, profile_home_page, normal_quote_pages, nsfw_quote_pages, hidden_quote_pages):
        #check if profile home buttons have timed out
        if home_page_buttons.page is None:
            if hidden==False:
                #if timed out delete message
                await message.delete()
            else:
                home_page_buttons.QuotePage.disabled = True
                home_page_buttons.NsfwPage.disabled = True
                home_page_buttons.add_item(discord.ui.Button(label="ㅤㅤㅤㅤㅤThis message has timed outㅤㅤㅤㅤ", row=2 ,style=discord.ButtonStyle.grey ,disabled=True))
                await message.edit(embed=profile_home_page, view=home_page_buttons)
                
            #if timed out place warning in console
            print(f'WARNING: home_page_buttons() view in server {interaction.guild.id} has timed out')
        #check if selected button is for normal quotes
        elif home_page_buttons.page == 1:
            
            current_page = 1    
            navigator=None
            #launch normal quote menu system
            await self.normal_quote_menu(interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages)

        elif home_page_buttons.page == 2:

            current_page = 1
            navigator=None
            await self.nsfw_quote_menu(interaction, hidden, message, navigator, nsfw_quote_pages, current_page, profile_home_page, normal_quote_pages, hidden_quote_pages)

        elif home_page_buttons.page == 3:
            current_page = 1
            navigator=None
            await self.hidden_quote_menu(interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages)

        else:
            print(f"WARNING: INVALID VALUE OF home_page_buttons.value in guild {interaction.guild.id} | value = {home_page_buttons.value}")
        

    async def normal_quote_menu(self, interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages):
            #set the navigation buttons
            navigator = self.PageNavigator(current_page, len(normal_quote_pages))
            if len(normal_quote_pages) == 1:
                #disable nav buttons if only 1 quote page
                navigator.Next.style = discord.ButtonStyle.grey
                navigator.Next.disabled = True
                navigator.Back.style = discord.ButtonStyle.grey
                navigator.Back.disabled = True                
            else:
                if current_page == 1:
                    #disabled back button since we shouldnt go back on page 1
                    navigator.Back.style = discord.ButtonStyle.grey
                    navigator.Back.disabled = True
                    #force enable next button
                    navigator.Next.style = discord.ButtonStyle.green
                    navigator.Next.disabled = False
                elif current_page == len(normal_quote_pages):
                    #disabled next button since we shouldnt go next on last page
                    navigator.Next.style = discord.ButtonStyle.grey
                    navigator.Next.disabled = True
                    #force enable back button
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False         

            #send normal quote page with navigation buttons
            await message.edit(embed=normal_quote_pages[current_page-1], view=navigator)
            #if navigation is Back increase page number
            await navigator.wait()
            if navigator.action == 1:
                current_page -= 1
                if current_page == 1:
                    navigator.Back.style = discord.ButtonStyle.grey
                    navigator.Back.disabled = True
                    navigator.Next.style = discord.ButtonStyle.green
                    navigator.Next.disabled = False
                else:
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False
                    
                #update message with new page number (current_page-1 because lists start at 0)
                await self.normal_quote_menu(interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages)
                # await self.normal_quote_menu(interaction, message, navigator, normal_quote_pages, current_page)

            #if navigation is Next increase page number
            elif navigator.action == 2:
                current_page += 1

                #update message with new page number (current_page-1 because lists start at 0)
                if current_page == len(normal_quote_pages):
                    navigator.Next.style = discord.ButtonStyle.grey
                    navigator.Next.disabled = True
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False
                else:
                    navigator.Next.style = discord.ButtonStyle.green
                    navigator.Next.disabled = False
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False


                await self.normal_quote_menu(interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages)
                # await self.normal_quote_menu(interaction, message, navigator, normal_quote_pages, current_page)

            elif navigator.action == 3:
                await self.profile_page(interaction, hidden, message, profile_home_page, normal_quote_pages, nsfw_quote_pages, hidden_quote_pages)

            elif navigator.action == None:
                if hidden==False:
                    #if timed out delete message
                    await message.delete()
                else:
                    navigator.Next.disabled = True
                    navigator.Back.disabled = True
                    navigator.Profile.disabled = True
                    navigator.add_item(discord.ui.Button(label="ㅤㅤㅤㅤㅤThis message has timed outㅤㅤㅤㅤ", row=2 ,style=discord.ButtonStyle.grey ,disabled=True))
                    await message.edit(view=navigator)

    #-------BUILD NSFW QUOTE MENU-------
    async def nsfw_quote_menu(self, interaction, hidden, message, navigator, nsfw_quote_pages, current_page, profile_home_page, normal_quote_pages, hidden_quote_pages):
            #set the navigation buttons
            navigator = self.PageNavigator(current_page, len(normal_quote_pages))
            if len(nsfw_quote_pages) == 1:
                #disable nav buttons if only 1 quote page
                navigator.Next.style = discord.ButtonStyle.grey
                navigator.Next.disabled = True
                navigator.Back.style = discord.ButtonStyle.grey
                navigator.Back.disabled = True                
            else:
                if current_page == 1:
                    #disabled back button since we shouldnt go back on page 1
                    navigator.Back.style = discord.ButtonStyle.grey
                    navigator.Back.disabled = True
                    #force enable next button
                    navigator.Next.style = discord.ButtonStyle.green
                    navigator.Next.disabled = False
                elif current_page == len(nsfw_quote_pages):
                    #disabled next button since we shouldnt go next on last page
                    navigator.Next.style = discord.ButtonStyle.grey
                    navigator.Next.disabled = True
                    #force enable back button
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False       
            #send normal quote page with navigation buttons
            await message.edit(embed=nsfw_quote_pages[current_page-1], view=navigator)
            #if navigation is Back increase page number
            await navigator.wait()
            if navigator.action == 1:
                current_page -= 1

                if current_page == 1:
                    navigator.Back.style = discord.ButtonStyle.grey
                    navigator.Back.disabled = True
                    navigator.Next.style = discord.ButtonStyle.green
                    navigator.Next.disabled = False
                else:
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False
                    
                #update message with new page number (current_page-1 because lists start at 0)
                await self.nsfw_quote_menu(interaction, hidden, message, navigator, nsfw_quote_pages, current_page, profile_home_page, normal_quote_pages, hidden_quote_pages)
                # await self.normal_quote_menu(interaction, message, navigator, normal_quote_pages, current_page)

            #if navigation is Next increase page number
            elif navigator.action == 2:
                current_page += 1

                #update message with new page number (current_page-1 because lists start at 0)
                if current_page == len(normal_quote_pages):
                    navigator.Next.style = discord.ButtonStyle.grey
                    navigator.Next.disabled = True
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False
                else:
                    navigator.Next.style = discord.ButtonStyle.green
                    navigator.Next.disabled = False
                    navigator.Back.style = discord.ButtonStyle.green
                    navigator.Back.disabled = False

                await self.nsfw_quote_menu(interaction, hidden, message, navigator, nsfw_quote_pages, current_page, profile_home_page, normal_quote_pages, hidden_quote_pages)

            elif navigator.action == 3:
                await self.profile_page(interaction, hidden, message, profile_home_page, normal_quote_pages, nsfw_quote_pages, hidden_quote_pages)

            elif navigator.action == None:
                if hidden==False:
                    #if timed out delete message
                    await message.delete()
                else:
                    navigator.Next.disabled = True
                    navigator.Back.disabled = True
                    navigator.Profile.disabled = True
                    navigator.add_item(discord.ui.Button(label="ㅤㅤㅤㅤㅤㅤThis message has timed outㅤㅤㅤㅤㅤ", row=2 ,style=discord.ButtonStyle.grey ,disabled=True))
                    await message.edit(view=navigator)

    async def hidden_quote_menu(self, interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages):
        #set the navigation buttons
        navigator = self.PageNavigator(current_page, len(hidden_quote_pages))
        if len(hidden_quote_pages) == 1:
            #disable nav buttons if only 1 quote page
            navigator.Next.style = discord.ButtonStyle.grey
            navigator.Next.disabled = True
            navigator.Back.style = discord.ButtonStyle.grey
            navigator.Back.disabled = True                
        else:
            if current_page == 1:
                #disabled back button since we shouldnt go back on page 1
                navigator.Back.style = discord.ButtonStyle.grey
                navigator.Back.disabled = True
                #force enable next button
                navigator.Next.style = discord.ButtonStyle.green
                navigator.Next.disabled = False
            elif current_page == len(hidden_quote_pages):
                #disabled next button since we shouldnt go next on last page
                navigator.Next.style = discord.ButtonStyle.grey
                navigator.Next.disabled = True
                #force enable back button
                navigator.Back.style = discord.ButtonStyle.green
                navigator.Back.disabled = False         

        #send hidden quote page with navigation buttons
        await message.edit(embed=hidden_quote_pages[current_page-1], view=navigator)
        #if navigation is Back increase page number
        await navigator.wait()
        if navigator.action == 1:
            current_page -= 1
            if current_page == 1:
                navigator.Back.style = discord.ButtonStyle.grey
                navigator.Back.disabled = True
                navigator.Next.style = discord.ButtonStyle.green
                navigator.Next.disabled = False
            else:
                navigator.Back.style = discord.ButtonStyle.green
                navigator.Back.disabled = False
                
            #update message with new page number (current_page-1 because lists start at 0)
            await self.hidden_quote_menu(interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages)

        #if navigation is Next increase page number
        elif navigator.action == 2:
            current_page += 1

            #update message with new page number (current_page-1 because lists start at 0)
            if current_page == len(hidden_quote_pages):
                navigator.Next.style = discord.ButtonStyle.grey
                navigator.Next.disabled = True
                navigator.Back.style = discord.ButtonStyle.green
                navigator.Back.disabled = False
            else:
                navigator.Next.style = discord.ButtonStyle.green
                navigator.Next.disabled = False
                navigator.Back.style = discord.ButtonStyle.green
                navigator.Back.disabled = False


            await self.hidden_quote_menu(interaction, hidden, message, navigator, normal_quote_pages, current_page, profile_home_page, nsfw_quote_pages, hidden_quote_pages)

        elif navigator.action == 3:
            await self.profile_page(interaction, hidden, message, profile_home_page, normal_quote_pages, nsfw_quote_pages, hidden_quote_pages)

        elif navigator.action == None:
            if hidden==False:
                #if timed out delete message
                await message.delete()
            else:
                navigator.Next.disabled = True
                navigator.Back.disabled = True
                navigator.Profile.disabled = True
                navigator.add_item(discord.ui.Button(label="ㅤㅤㅤㅤㅤThis message has timed outㅤㅤㅤㅤ", row=2 ,style=discord.ButtonStyle.grey ,disabled=True))
                await message.edit(view=navigator)


    #-----CREATE PROFILE MAIN PAGE BUTTONS-----

    class HomePageSelect(discord.ui.View):
        def __init__(self, timeout=300):
            super().__init__(timeout=timeout)
            self.page = None
            

        #Create button to see users normal quotes
        @discord.ui.button(label='Quotes', style=discord.ButtonStyle.blurple, row=1, emoji="<:quotes:994765517304889384>")
        async def QuotePage(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 1
            self.stop()

        #Create button to see users NSFW quotes
        @discord.ui.button(label='NSFW', style=discord.ButtonStyle.red, row=1, emoji="<:alert2:1016826438718066790>")
        async def NsfwPage(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 2
            self.stop()

        #Create button to see users badges
        @discord.ui.button(label='Deleted', style=discord.ButtonStyle.grey, row=1, emoji="<:blacklisted:1016829263707635742>")
        async def BadgesPage(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 3
            self.stop()
    
    #-----CREATE QUOTE PAGE NAVIGATION BUTTONS-----

    class PageNavigator(discord.ui.View):
        def __init__(self, current_page, end_page, timeout=120):
            super().__init__(timeout=timeout)
            self.action = None
            self.current_page = current_page
            self.end_page = end_page


        #Create button to see users normal quotes
        @discord.ui.button(label='Back', style=discord.ButtonStyle.green, disabled=False, emoji="<:previous:1014353821968896080>")
        async def Back(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.action = 1
            self.stop()

        #Create button to see users NSFW quotes
        @discord.ui.button(label='Next', style=discord.ButtonStyle.green, disabled=False, emoji="<:next:1014353798203985930>")
        async def Next(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.action = 2
            self.stop()

        #Create button to see users badges
        @discord.ui.button(label='Profile', row=2, style=discord.ButtonStyle.blurple, emoji="<:profile:1030032830891311174>")
        async def Profile(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.action = 3
            self.stop()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(user_lookup(bot), guilds = [discord.Object(id=838814770537824378)])