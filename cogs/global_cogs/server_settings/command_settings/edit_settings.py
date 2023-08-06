import discord
from discord import app_commands
from discord.ext import commands
import datetime
from humanize import precisedelta
import asyncio

class edit_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def edit_command_settings_menu(self, language_file, interaction, message, settings, setting_changed=(False, None)):
        server_settings = self.bot.get_cog('server_settings')
        command_selection_menu = self.bot.get_cog('server_command_settings')

        # get channels from settings
        command_cooldown_raw = settings['edit_command_cooldown']
        edit_timeout_raw = settings['edit_command_timeout']
        only_edit_added_raw = settings['only_edit_added']


        if command_cooldown_raw == 0:
            command_cooldown = "None"
        else:
            command_cooldown = f"{precisedelta(command_cooldown_raw, format='%0.0f')}"
        if edit_timeout_raw == 0:
            edit_timeout = "None"
        else:
            edit_timeout = f"{precisedelta(edit_timeout_raw, format='%0.0f')}"

        if only_edit_added_raw == True:
            only_edit_added = language_file['command_settings']['edit_settings']['only_edit_added_field_status'][0]
        else:
            only_edit_added = language_file['command_settings']['edit_settings']['only_edit_added_field_status'][1]

        # create embeds
        edit_command_settings_alert = discord.Embed(title="", description=f"{language_file['system_messages']['alert_message']}", color=0xff9b21)
       
        description = (
            "-\n" +
            f"{language_file['command_settings']['edit_settings']['cooldown_field']['name']}**{command_cooldown}**\n" +
            f"*{language_file['command_settings']['edit_settings']['cooldown_field']['value']}*\n\n" +
            f"{language_file['command_settings']['edit_settings']['edit_timeout_field']['name']}**{edit_timeout}**\n" +
            f"*{language_file['command_settings']['edit_settings']['edit_timeout_field']['value']}*\n\n" +
            f"{language_file['command_settings']['edit_settings']['only_edit_added_field']['name']}**{only_edit_added}**\n" +
            f"*{language_file['command_settings']['edit_settings']['only_edit_added_field']['value']}*\n" +
            "-\n" +
            f"{language_file['command_settings']['edit_settings']['description']}"
        )

        edit_command_embed = discord.Embed(title=f"{language_file['command_settings']['edit_settings']['title']}", description=description, color=0x6eb259)
        edit_command_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        edit_command_embed.timestamp = datetime.datetime.utcnow()
        edit_command_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        edit_command_dropdown = self.edit_command_dropdown(language_file, command_cooldown_raw, edit_timeout_raw, only_edit_added_raw)

        # edit message with dropdown and changed notif if language was changed
        if setting_changed != (False, None):
            edit_command_changed_embed = discord.Embed(title="", description=f"{language_file['command_settings']['setting_change_success'][0]} **{setting_changed[1]} {language_file['command_settings']['setting_change_success'][1]}**", color=0x068acc)
            await message.edit(embeds=[edit_command_settings_alert, edit_command_embed, edit_command_changed_embed], view=edit_command_dropdown)
        else:
            await message.edit(embeds=[edit_command_settings_alert, edit_command_embed], view=edit_command_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=[edit_command_settings_alert, edit_command_embed], view=edit_command_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await edit_command_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if edit_command_dropdown.selection == None and edit_command_dropdown.back == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server setting setting
        elif edit_command_dropdown.selection != None and edit_command_dropdown.back == None:
            
            #get the updated setting db key and embed name
            updated_setting = edit_command_dropdown.selection[1].split(":")
            updated_setting_id = edit_command_dropdown.selection[0]
            updated_setting_key = updated_setting[0]
            updated_setting_name = updated_setting[1]

            #update the corresponding channel setting
            await server_settings.update_server_settings(interaction.guild_id, updated_setting_key, updated_setting_id)
            
            settings = await server_settings.get_server_settings(interaction.guild_id)

            # reload the menu and inform user of setting change
            await self.edit_command_settings_menu(language_file, interaction, message, settings, setting_changed=(True, updated_setting_name))
            return

        elif edit_command_dropdown.back != None and edit_command_dropdown.selection == None:
            await command_selection_menu.command_settings(language_file, interaction, message, settings)
            return

        await self.edit_command_settings_menu(language_file, interaction, message, settings)


    class edit_command_dropdown(discord.ui.View):
        def __init__(self, language_file, current_cooldown, current_edit_timeout, current_oea, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.back = None
            self.language_file = language_file
            self.current_cooldown = current_cooldown
            self.current_edit_timeout = current_edit_timeout # delete from self
            self.current_oea = current_oea # only delete added

            cooldowns = [("None", 0), ("5sec", 5), ("10sec", 10), ("30sec", 30), ("1min", 60), ("5min", 300), ("10min", 600), ("30min", 1800), ("1hr", 3600), ("6hr", 21600), ("12hr", 43200), ("1day", 86400)]

            cooldown_options = [discord.SelectOption(
                label=self.language_file['command_settings']['edit_settings']['cooldown']['dropdown'][f'{cd_label}'], 
                value=cd_value,
                default=True if cd_value == self.current_cooldown else False
            ) for cd_label, cd_value in cooldowns]

            edit_timeout = [("None", 0), ("1min", 60), ("5min", 300), ("10min", 600), ("30min", 1800), ("1hr", 3600), ("6hr", 21600), ("12hr", 43200), ("1day", 86400)]

            edit_timeout_options = [discord.SelectOption(
                label=self.language_file['command_settings']['edit_settings']['cooldown']['dropdown'][f'{et_label}'], 
                value=et_value,
                default=True if et_value == self.current_edit_timeout else False
            ) for et_label, et_value in edit_timeout]
            
            only_edit_added_options = [
                discord.SelectOption(label=self.language_file['command_settings']['edit_settings']['only_edit_added']['dropdown']['enabled'], value=True, default=(True if self.current_oea == True else False)),
                discord.SelectOption(label=self.language_file['command_settings']['edit_settings']['only_edit_added']['dropdown']['disabled'], value=False, default=(True if self.current_oea == False else False))
                ]

            self.cooldown = discord.ui.Select(custom_id="edit_command_cooldown:Command Cooldown",min_values=1, max_values=1, options=cooldown_options)
            self.edit_timeout = discord.ui.Select(custom_id="edit_command_timeout:Edit Timeout",min_values=1, max_values=1, options=edit_timeout_options)
            self.only_edit_added = discord.ui.Select(custom_id="only_edit_added:Only Delete Added",min_values=1, max_values=1, options=only_edit_added_options)
            
            self.cooldown.callback = self.cooldown_dropdown
            self.edit_timeout.callback = self.edit_timeout_dropdown
            self.only_edit_added.callback = self.oea_dropdown
            
            self.add_item(self.cooldown)
            self.add_item(self.edit_timeout)
            self.add_item(self.only_edit_added)

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.edit_command_back
            self.add_item(self.back_button)

        async def cooldown_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            message = await interaction.original_response()
            loading_embed = discord.Embed(description=f"{self.language_file['system_messages']['processing_request']}", color=0x068acc)

            # Keep only the first 2 embeds
            message.embeds = message.embeds[:2]

            message.embeds.append(loading_embed)

            # Make sure to edit the message to actually display the new embed
            await message.edit(embeds=message.embeds, view=None)
            self.selection = (interaction.data['values'][0] if interaction.data['values'] else 0, interaction.data['custom_id'])
            self.stop()

        async def edit_timeout_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            message = await interaction.original_response()
            loading_embed = discord.Embed(description=f"{self.language_file['system_messages']['processing_request']}", color=0x068acc)

            # Keep only the first 2 embeds
            message.embeds = message.embeds[:2]

            message.embeds.append(loading_embed)

            # Make sure to edit the message to actually display the new embed
            await message.edit(embeds=message.embeds, view=None)
            self.selection = (interaction.data['values'][0] if interaction.data['values'] else True, interaction.data['custom_id'])
            self.stop()

        async def oea_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            message = await interaction.original_response()
            loading_embed = discord.Embed(description=f"{self.language_file['system_messages']['processing_request']}", color=0x068acc)

            # Keep only the first 2 embeds
            message.embeds = message.embeds[:2]

            message.embeds.append(loading_embed)

            # Make sure to edit the message to actually display the new embed
            await message.edit(embeds=message.embeds, view=None)
            self.selection = (interaction.data['values'][0] if interaction.data['values'] else True, interaction.data['custom_id'])
            self.stop()

        async def edit_command_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.back = 'back'
            self.stop()
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(edit_settings(bot), guilds = commands.Greedy[discord.Object])
