import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio

class profile_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def profile_command_settings_menu(self, language_file, interaction, message, settings, setting_changed=(False, None)):
        server_settings = self.bot.get_cog('server_settings')
        command_selection_menu = self.bot.get_cog('server_command_settings')

        # get channels from settings
        force_hidden_profile_raw = settings['force_hidden_profile']
        lock_nsfw_profile_raw = settings['lock_nsfw_profile']

        if force_hidden_profile_raw == True:
            force_hidden_profile = language_file['command_settings']['profile_settings']['force_hidden_profile_field_status'][0]
        else:
            force_hidden_profile = language_file['command_settings']['profile_settings']['force_hidden_profile_field_status'][1]

        if lock_nsfw_profile_raw == True:
            lock_nsfw_profile = language_file['command_settings']['profile_settings']['lock_nsfw_profile_field_status'][0]
        else:
            lock_nsfw_profile = language_file['command_settings']['profile_settings']['lock_nsfw_profile_field_status'][1]

        # create embeds
        profile_command_settings_alert = discord.Embed(title="", description=f"{language_file['system_messages']['alert_message']}", color=0xff9b21)
       
        description = f"-\n{language_file['command_settings']['profile_settings']['force_hidden_profile_field']['name']}**{force_hidden_profile}**\n*{language_file['command_settings']['profile_settings']['force_hidden_profile_field']['value']}*\n\n{language_file['command_settings']['profile_settings']['lock_nsfw_profile_field']['name']}**{lock_nsfw_profile}**\n*{language_file['command_settings']['profile_settings']['lock_nsfw_profile_field']['value']}*\n-\n{language_file['command_settings']['profile_settings']['description']}"
        profile_command_embed = discord.Embed(title=f"{language_file['command_settings']['profile_settings']['title']}", description=description, color=0x6eb259)
        profile_command_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        profile_command_embed.timestamp = datetime.datetime.utcnow()
        profile_command_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        profile_command_dropdown = self.profile_command_dropdown(language_file, force_hidden_profile_raw, lock_nsfw_profile_raw)

        # edit message with dropdown and changed notif if language was changed
        if setting_changed != (False, None):
            profile_command_changed_embed = discord.Embed(title="", description=f"{language_file['command_settings']['setting_change_success'][0]} **{setting_changed[1]} {language_file['command_settings']['setting_change_success'][1]}**", color=0x068acc)
            await message.edit(embeds=[profile_command_settings_alert, profile_command_embed, profile_command_changed_embed], view=profile_command_dropdown)
        else:
            await message.edit(embeds=[profile_command_settings_alert, profile_command_embed], view=profile_command_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=[profile_command_settings_alert, profile_command_embed], view=profile_command_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await profile_command_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if profile_command_dropdown.selection == None and profile_command_dropdown.back == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server setting setting
        elif profile_command_dropdown.selection != None and profile_command_dropdown.back == None:
            
            #get the updated setting db key and embed name
            updated_setting = profile_command_dropdown.selection[1].split(":")
            updated_setting_id = profile_command_dropdown.selection[0]
            updated_setting_key = updated_setting[0]
            updated_setting_name = updated_setting[1]

            #update the corresponding channel setting
            await server_settings.update_server_settings(interaction.guild_id, updated_setting_key, updated_setting_id)
            
            settings = await server_settings.get_server_settings(interaction.guild_id)

            # reload the menu and inform user of setting change
            await self.profile_command_settings_menu(language_file, interaction, message, settings, setting_changed=(True, updated_setting_name))
            return

        elif profile_command_dropdown.back != None and profile_command_dropdown.selection == None:
            await command_selection_menu.command_settings(language_file, interaction, message, settings)
            return

        await self.profile_command_settings_menu(language_file, interaction, message, settings)


    class profile_command_dropdown(discord.ui.View):
        def __init__(self, language_file, current_force_hidden, current_lock_nsfw, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.back = None
            self.language_file = language_file
            self.current_force_hidden = current_force_hidden
            self.current_lock_nsfw = current_lock_nsfw

            force_hidden_profile_options = [
                discord.SelectOption(label=self.language_file['command_settings']['profile_settings']['force_hidden_profile']['dropdown']['enabled'], value=True, default=(True if self.current_force_hidden == True else False)),
                discord.SelectOption(label=self.language_file['command_settings']['profile_settings']['force_hidden_profile']['dropdown']['disabled'], value=False, default=(True if self.current_force_hidden == False else False))
                ]
            
            lock_nsfw_profile_options = [
                discord.SelectOption(label=self.language_file['command_settings']['profile_settings']['lock_nsfw_profile']['dropdown']['enabled'], value=True, default=(True if self.current_lock_nsfw == True else False)),
                discord.SelectOption(label=self.language_file['command_settings']['profile_settings']['lock_nsfw_profile']['dropdown']['disabled'], value=False, default=(True if self.current_lock_nsfw == False else False))
                ]


            self.lock_nsfw_profile = discord.ui.Select(custom_id="lock_nsfw_profile:Lock NSFW",min_values=1, max_values=1, options=lock_nsfw_profile_options)
            self.force_hidden_profile = discord.ui.Select(custom_id="force_hidden_profile:Force Hidden Profile",min_values=1, max_values=1, options=force_hidden_profile_options)
            
            self.force_hidden_profile.callback = self.profile_settings_dropdown
            self.lock_nsfw_profile.callback = self.profile_settings_dropdown
            
            self.add_item(self.force_hidden_profile)
            self.add_item(self.lock_nsfw_profile)

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.profile_command_back
            self.add_item(self.back_button)

        async def profile_settings_dropdown(self, interaction: discord.Interaction):
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

        async def profile_command_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.back = 'back'
            self.stop()
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(profile_settings(bot), guilds = commands.Greedy[discord.Object])
