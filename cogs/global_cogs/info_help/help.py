import discord
import psycopg2
import humanize
from datetime import datetime
from discord import app_commands
from discord.ext import commands
import traceback as trace

class help_me(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def help_menu(self, interaction, hidden):
        #---------GET LANGUAGE---------
        language = self.bot.get_cog("language")
        #get server language
        server_language = await language.get_server_language(interaction.guild_id)
        #get language file
        language_file = await language.select_language(server_language, "commands\help\help_messages.json")

         #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description=f"{language_file['system_messages']['processing_request']}", color=0x068acc)
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
            is_bot_embed = discord.Embed(title=f"{language_file['system_messages']['no_bots']}", color=0xe02f2f)
            await message.edit(embed=is_bot_embed)
            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                return

        await self.help_page(message, interaction, language_file)

    async def help_page(self, message, interaction, language_file):
        #create main help menu
        main_help_menu = discord.Embed(title=f"{language_file['main_menu']['help_main_menu_title']}", description=f"{language_file['main_menu']['help_main_menu_desc']}", color=0x4381C1)
        main_help_menu.set_footer(text=f"{language_file['embed_footer']['footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        main_help_menu.timestamp = datetime.utcnow()

        #set dropdown object
        page_select = self.helpSelect(language_file)
        #send menu
        await message.edit(embed=main_help_menu, view=page_select)
        #wait for selection
        await page_select.wait()
        #display selected page
        await self.display_page(message, interaction, main_help_menu, page_select, language_file)

    async def display_page(self, message, interaction, home_page, page_select, language_file):

        #define new back button and dropdown menu
        select_dropdown_and_back_button = self.helpCommandDropdown(language_file)

        print(page_select.page, page_select.selection)

        #check to see if timed out
        if page_select.page is None and page_select.selection is None:
            
            # remove buttons and dropdown menus
            page_select.clear_items()

            # Add timeout notice
            page_select.add_item(discord.ui.Button(label=f"{language_file['system_messages']['timed_out']}", row=3, style=discord.ButtonStyle.grey, disabled=True))

            # Edit the original message with the new view object
            await message.edit(view=page_select)

        
        #check if back button was pressed
        elif page_select.page == 0 and page_select.selection is None:

            await self.help_page(message, interaction, language_file)

        #check if commands button was pressed
        elif page_select.page == 1 and page_select.selection is None:


            #create commands page
            commands_help = discord.Embed(title=f"{language_file['default_dropdown_page']['commands_default']['title']}", description=f"{language_file['default_dropdown_page']['commands_default']['desc']}", color=0x4381C1)
            commands_help.set_footer(text=f"{language_file['embed_footer']['footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            commands_help.timestamp = datetime.utcnow()

            #send commands help
            await message.edit(embed=commands_help, view=select_dropdown_and_back_button)
        
        elif page_select.page == 2 and page_select.selection is None:

            # Display Settings help page
            pass

        elif page_select.page == 3 and page_select.selection is None:

            # Display Alerts help page
            pass

        elif page_select.page == None and page_select.selection == "add_help":

            # Display Add command help page
            add_help_embed = discord.Embed(title=f"{language_file['commands_help_menus']['add_command_title']}", description=f"{language_file['commands_help_menus']['add_command_desc']}", color=0x4381C1)
            add_help_embed.set_footer(text=f"{language_file['embed_footer']['footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            add_help_embed.timestamp = datetime.utcnow()
            await message.edit(embed=add_help_embed, view=select_dropdown_and_back_button)

        elif page_select.page == None and page_select.selection == "delete_help":

            # Display Delete help page
            delete_help_embed = discord.Embed(title=f"{language_file['commands_help_menus']['delete_command_title']}", description=f"{language_file['commands_help_menus']['delete_command_desc']}", color=0x4381C1)
            delete_help_embed.set_footer(text=f"{language_file['embed_footer']['footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            delete_help_embed.timestamp = datetime.utcnow()
            await message.edit(embed=delete_help_embed, view=select_dropdown_and_back_button)


        elif page_select.page == None and page_select.selection == "profile_help":

            # Display Profile help page
            profile_help_embed = discord.Embed(title=f"{language_file['commands_help_menus']['profile_command_title']}", description=f"{language_file['commands_help_menus']['profile_command_desc']}", color=0x4381C1)
            profile_help_embed.set_footer(text=f"{language_file['embed_footer']['footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            profile_help_embed.timestamp = datetime.utcnow()
            await message.edit(embed=profile_help_embed, view=select_dropdown_and_back_button)

        else:

            # error page and msg
            error_embed = discord.Embed(title=f"{language_file['system_messages']['error_title']}", description=f"{language_file['system_messages']['error_desc']}", color=0xe02f2f)
            await message.edit(embed=error_embed, view=None)
            print("Error in help.py, display_page function")
            return

        await select_dropdown_and_back_button.wait()

        await self.display_page(message, interaction, home_page, select_dropdown_and_back_button, language_file)
          
#-------------help MENU BUTTON---------------

    class helpSelect(discord.ui.View):
        def __init__(self, language_file, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.page = None
            self.language_file = language_file

            # Create buttons and assign callbacks
            command_button = discord.ui.Button(label=self.language_file['menu_buttons']['commands_category_button'], style=discord.ButtonStyle.green, row=1)
            command_button.callback = self.command_help
            self.add_item(command_button)

            settings_button = discord.ui.Button(label=self.language_file['menu_buttons']['settings_category_button'], style=discord.ButtonStyle.blurple, row=1)
            settings_button.callback = self.settings_help
            self.add_item(settings_button)

            alerts_button = discord.ui.Button(label=self.language_file['menu_buttons']['alerts_category_button'], style=discord.ButtonStyle.red, row=1)
            alerts_button.callback = self.alerts_help
            self.add_item(alerts_button)

        async def command_help(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 1
            self.stop()

        async def settings_help(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 2
            self.stop()

        async def alerts_help(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 3
            self.stop()


        
#-------------command selection dropdown---------------

    class helpCommandDropdown(discord.ui.View):
        def __init__(self, language_file, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.page = None
            self.language_file = language_file

            command_options = [
                discord.SelectOption(label=self.language_file['commands_dropdown']['add_command']['title'], description=self.language_file['commands_dropdown']['add_command']['desc'], value="add_help"),
                discord.SelectOption(label=self.language_file['commands_dropdown']['delete_command']['title'], description=self.language_file['commands_dropdown']['delete_command']['desc'], value="delete_help"),
                discord.SelectOption(label=self.language_file['commands_dropdown']['profile_command']['title'], description=self.language_file['commands_dropdown']['profile_command']['desc'], value="profile_help")
            ]

            self.select = discord.ui.Select(placeholder=self.language_file['commands_dropdown']['dropdown_placeholder'], options=command_options, min_values=1, max_values=1)
            self.select.callback = self.command_dropdown
            self.add_item(self.select)

            self.back_button = discord.ui.Button(label=self.language_file['menu_buttons']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.help_back
            self.add_item(self.back_button)

        async def command_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = interaction.data['values'][0] if interaction.data['values'][0] else None
            self.stop()

        async def help_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 0
            self.stop()





async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(help_me(bot), guilds = commands.Greedy[discord.Object])
