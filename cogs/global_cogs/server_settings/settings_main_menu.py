import discord
import datetime
import json
from discord import app_commands
from discord.ext import commands
import psycopg2.extras

class server_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def get_server_settings(self, guild_id):
        #check db for server settings
        #set database variable
        database = self.bot.get_cog("database")

        #get server language setting
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #create query to get user informtion
        command = f"select * from guild_settings where guild_id={guild_id}"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        if results:

            server_settings = results[0]
        else:
            #######################################################################################################
            ## create and load default server settings for that server then send a follow up message to the user ##
            ##    to let them know that the server settings have been created and that they can now edit them    ##
            #######################################################################################################
            pass

        #return the server language setting
        return server_settings

    async def update_server_settings(self, guild_id, setting, new_value):
        #check db for server settings
        if new_value == None and (setting == "added_quotes_channel" or setting == "action_log_channel" or setting == "alerts_channel"):
            new_value = -1
        elif new_value == None:
            new_value = "None"
        #set database variable
        database = self.bot.get_cog("database")
        #get server language setting
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query to get user informtion
        command = f"update guild_settings set {setting}={new_value} where guild_id={guild_id}"
        #execute command
        c.execute(command)
        #get results of query
        conn.commit()
        #close database connection
        c.close()
        conn.close()

    async def edit_server_settings(self, interaction):
        #---------GET LANGUAGE---------
        language = self.bot.get_cog("language")
        #get server language
        server_language = await language.get_server_language(interaction.guild_id)
        #get language file
        language_file = await language.select_language(server_language, "settings_messages.json")

         #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description=f"{language_file['system_messages']['processing_request']}", color=0x068acc)
        #Send loading message
        await interaction.response.send_message(embed=loading_embed, ephemeral=True)
        #assign message for future edits
        message = await interaction.original_response()

        #------Pass System Checks-----
        #check maintenance
        #check if user is a bot
        if interaction.user.bot:
            #if is a bot cancel request
            is_bot_embed = discord.Embed(title=f"{language_file['system_messages']['no_bots']}", color=0xe02f2f)
            await message.edit(embed=is_bot_embed)

        #check if user has permission to edit server settings
        # TO BE IMPLEMENTED

        settings = await self.get_server_settings(interaction.guild_id)

        await self.settings_main_menu(language_file, interaction, message, settings)

    
    async def settings_main_menu(self, language_file, interaction, message, settings):

        settings_embed = discord.Embed(title=f"{language_file['settings_main_menu']['title']}", description=f"{language_file['settings_main_menu']['description']}", color=0x6eb259)
        settings_embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
        settings_embed.timestamp = datetime.datetime.utcnow()
        settings_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        mm_dropdown = self.main_menu_dropdown(language_file)

        #edit message with dropdown
        await message.edit(embed=settings_embed, view=mm_dropdown)

        #wait for user to select an option
        await mm_dropdown.wait()

        #check if user selected an option
        if mm_dropdown.selection == None:
            timed_out = self.timed_out(language_file)
            #time out the message
            await message.edit(view=timed_out)
            return
        else:
            # display the selected page
            await self.display_settings_page(language_file, interaction, message, settings, mm_dropdown.selection)


    async def display_settings_page(self, language_file, interaction, message, settings, selection):

        if selection == "language_settings":
            server_language_settings = self.bot.get_cog('server_language_settings')
            await server_language_settings.language_settings(language_file, interaction, message, settings)

        elif selection == "channel_settings":
            server_channel_settings = self.bot.get_cog('channel_settings')
            await server_channel_settings.channel_settings_menu(language_file, interaction, message, settings)

        elif selection == "command_settings":
            server_command_settings = self.bot.get_cog('server_command_settings')
            await server_command_settings.command_settings(language_file, interaction, message, settings)

        elif selection == "detection_settings":
            server_filter_settings = self.bot.get_cog('server_filter_settings')
            await server_filter_settings.filter_settings(language_file, interaction, message, settings)

        # elif selection == "automod_settings":
        #     await self.automod_settings(language_file, interaction, message, settings)

        elif selection == "main_menu":
            await self.settings_main_menu(language_file, interaction, message, settings)

        else:
            await self.settings_main_menu(language_file, interaction, message, settings)


    class timed_out(discord.ui.View):
        def __init__(self, language_file):
            super().__init__()
            self.language_file = language_file
            self.timed_out = discord.ui.Button(label=self.language_file['system_messages']['timed_out'], style=discord.ButtonStyle.grey, disabled=True)
            self.add_item(self.timed_out)

    class main_menu_dropdown(discord.ui.View):
        def __init__(self, language_file, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.language_file = language_file

            settings_options = [
                # create a select option for each dropdown category: language, channel, community, commands, detection, automod
                discord.SelectOption(label=self.language_file['settings_main_menu']['dropdown']['language'][0], description=self.language_file['settings_main_menu']['dropdown']['language'][1], value="language_settings"),
                discord.SelectOption(label=self.language_file['settings_main_menu']['dropdown']['channel'][0], description=self.language_file['settings_main_menu']['dropdown']['channel'][1], value="channel_settings"),
                discord.SelectOption(label=self.language_file['settings_main_menu']['dropdown']['commands'][0], description=self.language_file['settings_main_menu']['dropdown']['commands'][1], value="command_settings"),
                discord.SelectOption(label=self.language_file['settings_main_menu']['dropdown']['detection'][0], description=self.language_file['settings_main_menu']['dropdown']['detection'][1], value="detection_settings"),
                discord.SelectOption(label=self.language_file['settings_main_menu']['dropdown']['automod'][0], description=self.language_file['settings_main_menu']['dropdown']['automod'][1], value="automod_settings"),
            ]

            self.select = discord.ui.Select(placeholder=self.language_file['settings_main_menu']['dropdown']['dropdown_placeholder'], options=settings_options, min_values=1, max_values=1)
            self.select.callback = self.settings_dropdown
            self.add_item(self.select)

        async def settings_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = interaction.data['values'][0] if interaction.data['values'][0] else None
            self.stop()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_settings(bot), guilds=commands.Greedy[discord.Object])
