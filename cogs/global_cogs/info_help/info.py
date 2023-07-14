import discord
import psycopg2
import humanize
from datetime import datetime
from discord import app_commands
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def info_menu(self, interaction, hidden):
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
        #check maintenance
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

        await self.info_page(message, interaction)

    async def info_page(self, message, interaction):
        #create main info menu
        main_info_menu = discord.Embed(title="QuoteBot information Navigator", description="Use the buttons below to get info with commands or learn more about QuoteBot", color=0x4381C1)
        main_info_menu.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        main_info_menu.timestamp = datetime.utcnow()

        #set button object
        page_select = self.infoSelect()
        #send menu
        await message.edit(embed=main_info_menu, view=page_select)
        #wait for selection
        await page_select.wait()
        #display selected page
        await self.display_page(message, interaction, main_info_menu, page_select)

    async def display_page(self, message, interaction, home_page, page_select):

        #define back button
        back_button = self.infoBack()

        #check to see if timed out
        if page_select.page is None:
            
            #disable all buttons
            try:
                page_select.nsfw_info.disabled = True
                page_select.blocked_info.disabled = True
                page_select.blacklist_info.disabled = True
                page_select.bot_info.disabled = True
                page_select.changelog.disabled = True
            except:
                page_select.info_back.disabled = True
            #add timeout notice
            page_select.add_item(discord.ui.Button(label="ㅤㅤㅤㅤㅤThis message has timed outㅤㅤㅤㅤ", row=3 ,style=discord.ButtonStyle.grey ,disabled=True))
            #send timeout edit
            await message.edit(view=page_select)
        
        #check if back button was pressed
        elif page_select.page == 0:

            await self.info_page(message, interaction)

        #check if nsfw button was pressed
        elif page_select.page == 1:


            #create nsfw page
            desc = "While QuoteBot does not have strict rules on what can and can't be added we do split quotes into Normal and NSFW categories in an effort to better sort quotes by their content. If your quote contains slurs or other vulgar language it will be placed into the NSFW category. Quotes marked as NSFW cannot be added as a pinned quote. *Swearing and semi-vulgar language will not be filtered!*\n\n**NOTE** This system is not perfect and can make mistakes, If you think a quote was mistakenly placed in the NSFW category please contact me: **__vexi#0420__**"
            nsfw_info = discord.Embed(title="NSFW Category info", description=desc, color=0x4381C1)
            nsfw_info.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            nsfw_info.timestamp = datetime.utcnow()

            #send nsfw info
            await message.edit(embed=nsfw_info, view=back_button)
        
        #check if blocked button was pressed
        elif page_select.page == 2:
            

            #create nsfw page
            desc = "While QuoteBot does not have strict rules, due to security and privacy reasons, if your quote includes any of the following it will be blocked from being added.\n__Blocked content:__\n- Links of any kind\n- Personal information (email, ip, etc)\n\n**Excessive attempts or attempting to bypass the filter may result in a blacklist (See Blacklist info)**"
            blocked_info = discord.Embed(title="Blocked Quotes info", description=desc, color=0x4381C1)
            blocked_info.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            blocked_info.timestamp = datetime.utcnow()

            #send nsfw info
            await message.edit(embed=blocked_info, view=back_button)

        #check if blacklist button was pressed
        elif page_select.page == 3:
            

            #create nsfw page
            desc = "If we find or recieve excessive reports of a user abusing our systems in any way: spamming, blackmail, doxxing, etc. We reserve the right to blacklist that user. Being blacklisted means that you will no longer be able to access QuoteBot and your profile will be locked too all users."
            blacklist_info = discord.Embed(title="QuoteBot Blacklist info", description=desc, color=0x4381C1)
            blacklist_info.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            blacklist_info.timestamp = datetime.utcnow()

            #send nsfw info
            await message.edit(embed=blacklist_info, view=back_button)

        #check if bot button was pressed
        elif page_select.page == 4:
            
            #display loading message
            loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Gathering Bot info**", color=0x068acc)
            #Send loading message
            await message.edit(embed=loading_embed, view=None)

            bot_stats = await self.get_bot_stats()

            #create bot page
            bot_info = discord.Embed(title="QuoteBot info", description="-",color=0x4381C1)
            bot_info.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            bot_info.timestamp = datetime.utcnow()
            
            for key in bot_stats.keys():
                bot_info.add_field(name=f"{str(key).replace('_',' ')}: {bot_stats[key]}", value="\u200B", inline=False)

            #send nsfw info
            await message.edit(embed=bot_info, view=back_button)

        #check if changelog button was pressed
        elif page_select.page == 5:
            

            #create changelog page
            changelog = discord.Embed(title="CHANGELOG")
            changelog.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            changelog.timestamp = datetime.utcnow()
            

            #send nsfw info
            await message.edit(embed=changelog, view=back_button)
        
        await back_button.wait()
        await self.display_page(message, interaction, home_page, back_button)
          
#-------------BOT STAT COLLECTOR------------

    async def get_bot_stats(self):

        #define empty dict
        stats = {}

        # --------------------
        # | get server count |
        # --------------------
        server_count = len(self.bot.guilds)
        stats['Server_Count'] = server_count

        # ------------------
        # | get user count |
        # ------------------
        #define database variable
        database = self.bot.get_cog("database")
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all distinct quotes
        command = f"SELECT COUNT(*) FROM (SELECT DISTINCT uid FROM quotes where hidden=False) AS temp"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        count = results
        stats['User_Count'] = count[0][0]

        # -------------------
        # | get quote count |
        # -------------------
        #create query for all non nsfw quotes
        command = f"SELECT COUNT(*) FROM (SELECT DISTINCT quote FROM quotes where hidden=False) AS temp"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()
        count = results
        stats['Quote_Count'] = count[0][0]

        # ------------------------
        # | get database latency |
        # ------------------------
        start = datetime.now()
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all quotes
        command = f"select * from quotes"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()
        end = datetime.now()
        total_time = humanize.naturaldelta(end-start, minimum_unit="milliseconds")
        stats["Database_Latency"] = total_time

        # ----------------------
        # | get filter latency |
        # ----------------------
        #set content filter variable
        content_filter = self.bot.get_cog("content_filter")
        start = datetime.now()
        #send quote to filter api
        await content_filter.check_nsfw("#LATENCY CHECK# f@g")
        end = datetime.now()
        total_time = humanize.naturaldelta(end-start, minimum_unit="milliseconds")
        stats["Filter_Latency"] = total_time

        return(stats)

#-------------info MENU BUTTON---------------

    class infoSelect(discord.ui.View):
        def __init__(self, timeout=300):
            super().__init__(timeout=timeout)
            self.page = None
            
        #Display info about QuoteBot's NSFW Category and Policy
        @discord.ui.button(label='NSFW', style=discord.ButtonStyle.blurple, row=1, emoji="<:alert2:1016826438718066790>")
        async def nsfw_info(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 1
            self.stop()
        
        #Display info about QuoteBot's blocked quote policy
        @discord.ui.button(label='Blocked', style=discord.ButtonStyle.blurple, row=1, emoji="<:alert:994765426829561928>")
        async def blocked_info(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 2
            self.stop()

        #Display info about QuoteBot's blacklist policy
        @discord.ui.button(label='Blacklist', style=discord.ButtonStyle.blurple, row=1, emoji="<:blacklisted:1016829263707635742>")
        async def blacklist_info(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 3
            self.stop()

        #Display background info about QuoteBot (latency, server count, quotecount, version, etc) 
        @discord.ui.button(label='Bot Stats', style=discord.ButtonStyle.blurple, row=2, emoji="<:stats:1028937500661665883>")
        async def bot_info(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 4
            self.stop()

        #Display QuoteBot's most recent update announcement
        @discord.ui.button(label='Updates/Changelog', style=discord.ButtonStyle.blurple, row=2, disabled=True, emoji="<:download:1028937521268281345>  ")
        async def changelog(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 5
            self.stop()
        
#-------------Back Button------------

    class infoBack(discord.ui.View):
        def __init__(self, timeout=300):
            super().__init__(timeout=timeout)
            self.page = None

        #Create button to see users badges
        @discord.ui.button(label='Back', row=2, style=discord.ButtonStyle.blurple, emoji="<:info_back:1028918526238523433>")
        async def info_back(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.page = 0
            self.stop()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(info(bot), guilds = commands.Greedy[discord.Object])
