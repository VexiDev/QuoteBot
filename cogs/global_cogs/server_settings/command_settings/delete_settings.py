import discord
from discord import app_commands
from discord.ext import commands
import datetime
from humanize import precisedelta
import asyncio

class delete_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def delete_command_settings_menu(self, language_file, interaction, message, settings, setting_changed=(False, None)):
        server_settings = self.bot.get_cog('server_settings')
        command_selection_menu = self.bot.get_cog('server_command_settings')

        # get channels from settings
        command_cooldown_raw = settings['delete_command_cooldown']
        delete_from_self_raw = settings['delete_from_self']
        only_delete_added_raw = settings['only_delete_added']


        if command_cooldown_raw == 0:
            command_cooldown = "None"
        else:
            command_cooldown = f"{precisedelta(command_cooldown_raw, format='%0.0f')}"
        if delete_from_self_raw == True:
            delete_from_self = language_file['command_settings']['delete_settings']['delete_from_self_field_status'][0]
        else:
            delete_from_self = language_file['command_settings']['delete_settings']['delete_from_self_field_status'][1]
        if only_delete_added_raw == True:
            only_delete_added = language_file['command_settings']['delete_settings']['only_delete_added_field_status'][0]
        else:
            only_delete_added = language_file['command_settings']['delete_settings']['only_delete_added_field_status'][1]

        # create embeds
        delete_command_settings_alert = discord.Embed(title="", description=f"{language_file['system_messages']['alert_message']}", color=0xff9b21)
       
        description = (
            "-\n" +
            f"{language_file['command_settings']['delete_settings']['cooldown_field']['name']}**{command_cooldown}**\n" +
            f"*{language_file['command_settings']['delete_settings']['cooldown_field']['value']}*\n\n" +
            f"{language_file['command_settings']['delete_settings']['only_delete_added_field']['name']}**{only_delete_added}**\n" +
            f"*{language_file['command_settings']['delete_settings']['only_delete_added_field']['value']}*\n\n" +
            f"{language_file['command_settings']['delete_settings']['delete_from_self_field']['name']}**{delete_from_self}**\n" +
            f"*{language_file['command_settings']['delete_settings']['delete_from_self_field']['value']}*\n" +
            "-\n" +
            f"{language_file['command_settings']['delete_settings']['description']}"
        )

        delete_command_embed = discord.Embed(title=f"{language_file['command_settings']['delete_settings']['title']}", description=description, color=0x6eb259)
        delete_command_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        delete_command_embed.timestamp = datetime.datetime.utcnow()
        delete_command_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        delete_command_dropdown = self.delete_command_dropdown(language_file, command_cooldown_raw, delete_from_self_raw, only_delete_added_raw)

        # edit message with dropdown and changed notif if language was changed
        if setting_changed != (False, None):
            delete_command_changed_embed = discord.Embed(title="", description=f"{language_file['command_settings']['setting_change_success'][0]} **{setting_changed[1]} {language_file['command_settings']['setting_change_success'][1]}**", color=0x068acc)
            await message.edit(embeds=[delete_command_settings_alert, delete_command_embed, delete_command_changed_embed], view=delete_command_dropdown)
        else:
            await message.edit(embeds=[delete_command_settings_alert, delete_command_embed], view=delete_command_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=[delete_command_settings_alert, delete_command_embed], view=delete_command_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await delete_command_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if delete_command_dropdown.selection == None and delete_command_dropdown.back == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server setting setting
        elif delete_command_dropdown.selection != None and delete_command_dropdown.back == None:
            
            #get the updated setting db key and embed name
            updated_setting = delete_command_dropdown.selection[1].split(":")
            updated_setting_id = delete_command_dropdown.selection[0]
            updated_setting_key = updated_setting[0]
            updated_setting_name = updated_setting[1]

            #update the corresponding channel setting
            await server_settings.update_server_settings(interaction.guild_id, updated_setting_key, updated_setting_id)
            
            settings = await server_settings.get_server_settings(interaction.guild_id)

            # reload the menu and inform user of setting change
            await self.delete_command_settings_menu(language_file, interaction, message, settings, setting_changed=(True, updated_setting_name))
            return

        elif delete_command_dropdown.back != None and delete_command_dropdown.selection == None:
            await command_selection_menu.command_settings(language_file, interaction, message, settings)
            return

        await self.delete_command_settings_menu(language_file, interaction, message, settings)


    class delete_command_dropdown(discord.ui.View):
        def __init__(self, language_file, current_cooldown, current_dfs, current_oda, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.back = None
            self.language_file = language_file
            self.current_cooldown = current_cooldown
            self.current_dfs = current_dfs # delete from self
            self.current_oda = current_oda # only delete added

            cooldowns = [("None", 0), ("5sec", 5), ("10sec", 10), ("30sec", 30), ("1min", 60), ("5min", 300), ("10min", 600), ("30min", 1800), ("1hr", 3600), ("6hr", 21600), ("12hr", 43200), ("1day", 86400)]

            cooldown_options = [discord.SelectOption(
                label=self.language_file['command_settings']['delete_settings']['cooldown']['dropdown'][f'{cd_label}'], 
                value=cd_value,
                default=True if cd_value == self.current_cooldown else False
            ) for cd_label, cd_value in cooldowns]

            delete_from_self_options = [
                discord.SelectOption(label=self.language_file['command_settings']['delete_settings']['delete_from_self']['dropdown']['enabled'], value=True, default=(True if self.current_dfs == True else False)),
                discord.SelectOption(label=self.language_file['command_settings']['delete_settings']['delete_from_self']['dropdown']['disabled'], value=False, default=(True if self.current_dfs == False else False))
                ]
            
            only_delete_added_options = [
                discord.SelectOption(label=self.language_file['command_settings']['delete_settings']['only_delete_added']['dropdown']['enabled'], value=True, default=(True if self.current_oda == True else False)),
                discord.SelectOption(label=self.language_file['command_settings']['delete_settings']['only_delete_added']['dropdown']['disabled'], value=False, default=(True if self.current_oda == False else False))
                ]

            self.cooldown = discord.ui.Select(custom_id="delete_command_cooldown:Command Cooldown",min_values=1, max_values=1, options=cooldown_options)
            self.delete_from_self = discord.ui.Select(custom_id="delete_from_self:Delete from Self",min_values=1, max_values=1, options=delete_from_self_options)
            self.only_delete_added = discord.ui.Select(custom_id="only_delete_added:Only Delete Added",min_values=1, max_values=1, options=only_delete_added_options)
            
            self.cooldown.callback = self.cooldown_dropdown
            self.delete_from_self.callback = self.dfs_dropdown
            self.only_delete_added.callback = self.oda_dropdown
            
            self.add_item(self.cooldown)
            self.add_item(self.only_delete_added)
            self.add_item(self.delete_from_self)

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.delete_command_back
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

        async def dfs_dropdown(self, interaction: discord.Interaction):
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

        async def oda_dropdown(self, interaction: discord.Interaction):
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

        async def delete_command_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.back = 'back'
            self.stop()
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(delete_settings(bot), guilds = commands.Greedy[discord.Object])
