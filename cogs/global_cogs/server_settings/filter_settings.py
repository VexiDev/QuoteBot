import discord
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands

class server_filter_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.PRESET_ACTIONS = {
        "Default": {
            "h_derogatory": ["Warn"],
            "h_threats": ["Warn"],
            "sexual_content": ["Warn"],
            "sensitive": ["Warn"]
        },
        "Light": {
            "h_derogatory": ["Cancel", "Notify"]
        },
        "Medium": {
            "h_profanity": ["Warn", "Hold"],
            "sexual_content": ["Warn", "Hold"],
            "h_derogatory": ["Warn", "Hold"],
            "l_derogatory": ["Warn", "Hold"]
        },
        "Strict": {
            "l_threats": ["Warn", "Hold"],
            "h_threats": ["Cancel", "Notify"],
            "light_sexual_content": ["Warn", "Hold"],
            "sexual_content": ["Cancel", "Notify"],
            "l_profanity": ["Warn", "Hold"],
            "h_profanity": ["Cancel", "Notify"],
            "sensitive": ["Warn", "Hold"],
            "h_derogatory": ["Cancel", "Notify"],
            "l_derogatory": ["Cancel", "Notify"]
        },
        "Custom": {}
    }

    async def filter_settings(self, language_file, interaction, message, settings, filter_changed=(False, None)):
        server_settings = self.bot.get_cog('server_settings')

        # create embed
        description = f"{language_file['filter_settings']['description']['header']}**{language_file['filter_settings']['description']['preset']}** {settings['filter_preset_name']}\n{language_file['filter_settings']['description']['preset_desc'][settings['filter_preset_name']]}{language_file['filter_settings']['description']['end']}"
        filter_embed = discord.Embed(title=f"{language_file['filter_settings']['title']}", description=description, color=0x6eb259)
        filter_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        filter_embed.timestamp = datetime.datetime.utcnow()
        filter_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        current_filter_settings = {
            'preset': settings['filter_preset_name'], #string
            'settings': settings['filter_detection_types']
        }

        #create dropdown
        filter_dropdown = self.filter_dropdown(language_file, current_filter_settings)

        # warn user of possible ( but unlikely i hope :] ) filter inaccuracy
        inaccuracy_warning_embed = discord.Embed(title="", description=f"{language_file['filter_settings']['inaccuracy_warning']}", color=0xff9b21)
        
        # edit message with dropdown and changed notif if filter was changed
        if filter_changed != (False, None):
            if filter_changed[1] == "":
                filter_changed_embed = discord.Embed(title="", description=f"**{language_file['filter_settings']['custom_dropdown']['applied']}**", color=0x068acc)
            else:
                filter_changed_embed = discord.Embed(title="", description=f"{language_file['filter_settings']['preset_dropdown']['applied'][0]} **{filter_changed[1]} {language_file['filter_settings']['preset_dropdown']['applied'][1]}**", color=0x068acc)
            await message.edit(embeds=[inaccuracy_warning_embed, filter_embed, filter_changed_embed], view=filter_dropdown)
        else:
            await message.edit(embeds=[inaccuracy_warning_embed, filter_embed], view=filter_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=[inaccuracy_warning_embed, filter_embed], view=filter_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await filter_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if filter_dropdown.selection == None and filter_dropdown.preset == None and filter_dropdown.back == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server filter setting
        elif filter_dropdown.selection != None and settings['filter_preset_name'] == "Custom" and filter_dropdown.back == None:

            #prepare list for postegres
            type_list = '{' + ', '.join(f'"{item}"' for item in filter_dropdown.selection) + '}'

            #update the server filter settings with the new preset/filter
            await server_settings.update_server_settings(interaction.guild_id, "filter_detection_types", f"\'{type_list}\'")

            settings = await server_settings.get_server_settings(interaction.guild_id)

            await self.filter_settings(language_file, interaction, message, settings, filter_changed=(True, ""))
            return

        elif filter_dropdown.selection == None and filter_dropdown.preset != None and filter_dropdown.back == None:
            if filter_dropdown.preset == 'Custom':
                preset_actions = {}
            else:
                preset_actions = self.PRESET_ACTIONS.get(filter_dropdown.preset, self.PRESET_ACTIONS["Default"])

            updates = []

            # If preset_actions is not empty, add its keys to type_list and perform the updates
            if preset_actions:
                type_list = '{"' + '", "'.join(preset_actions.keys()) + '"}'
                for detection_type, actions in preset_actions.items():
                    action_list = '{"' + '", "'.join(actions) + '"}'
                    updates.append((f"automod_{detection_type}_actions", f"\'{action_list}\'"))

                updates.append(("filter_detection_types", f"\'{type_list}\'"))
            else:
                # If preset_actions is empty (which means the 'Custom' preset was selected), set type_list to '{}'
                updates.append(("filter_detection_types", "'{}'"))

            updates.append(("filter_preset_name", f"\'{filter_dropdown.preset}\'"))

            await server_settings.update_server_settings_batch(interaction.guild_id, updates)

            settings = await server_settings.get_server_settings(interaction.guild_id)
            await self.filter_settings(language_file, interaction, message, settings, filter_changed=(True, filter_dropdown.preset))
            return
        
        elif filter_dropdown.back != None and filter_dropdown.selection == None and filter_dropdown.preset == None:
            await server_settings.settings_main_menu(language_file, interaction, message, settings)
            return

        await self.filter_settings(language_file, interaction, message, settings, filter_changed=(False, None))

    class filter_dropdown(discord.ui.View):
        def __init__(self, language_file, current_filter_settings=['None'], timeout=180):
            super().__init__(timeout=timeout)
            self.selection = None
            self.preset = None
            self.back = None
            self.language_file = language_file
            self.current_filter_settings = current_filter_settings

            preset_list = ['Default', 'Light', 'Medium', 'Strict', 'Custom']

            preset_options = [
                discord.SelectOption(
                    label=self.language_file['filter_settings']['preset_dropdown'][preset]['label'],
                    description=self.language_file['filter_settings']['preset_dropdown'][preset]['desc'],
                    value=preset,
                    default=True if preset == self.current_filter_settings['preset'] else False
                ) for preset in preset_list
            ]

            self.preset_select = discord.ui.Select(placeholder=self.language_file['filter_settings']['preset_dropdown']['placeholder'], options=preset_options, min_values=1, max_values=1)
            self.preset_select.callback = self.preset_dropdown
            self.add_item(self.preset_select)

            filter_types = ['l_profanity', 'h_profanity', 'light_sexual_content', 'sexual_content', 'l_threats', 'h_threats', 'l_derogatory','h_derogatory', 'sensitive']

            filter_options = [discord.SelectOption(
                label=self.language_file['filter_settings']['custom_dropdown'][f_type]['label'], 
                description=self.language_file['filter_settings']['custom_dropdown'][f_type]['desc'],
                value=f'{f_type}', 
                default=True if f_type in self.current_filter_settings['settings'] else False
            ) for f_type in filter_types]

            self.custom_select = discord.ui.Select(placeholder=self.language_file['filter_settings']['custom_dropdown']['placeholder'], options=filter_options, min_values=0, max_values=len(filter_types))
            self.custom_select.callback = self.custom_dropdown
            self.add_item(self.custom_select)           
            if self.current_filter_settings['preset'] != 'Custom':
                self.custom_select.disabled = True

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.filter_back
            self.add_item(self.back_button)

        async def custom_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            message = await interaction.original_response()
            loading_embed = discord.Embed(description=f"{self.language_file['system_messages']['processing_request']}", color=0x068acc)

            # Keep only the first 2 embeds
            message.embeds = message.embeds[:2]

            message.embeds.append(loading_embed)

            # Make sure to edit the message to actually display the new embed
            await message.edit(embeds=message.embeds, view=None)
            self.selection = interaction.data['values'] if interaction.data['values'] else 'error'
            self.stop()

        async def preset_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            
            message = await interaction.original_response()
            loading_embed = discord.Embed(description=f"{self.language_file['system_messages']['processing_request']}", color=0x068acc)

            # Keep only the first 2 embeds
            message.embeds = message.embeds[:2]

            message.embeds.append(loading_embed)

            # Make sure to edit the message to actually display the new embed
            await message.edit(embeds=message.embeds, view=None)

            self.preset = interaction.data['values'][0] if interaction.data['values'][0] else 'Default'
            self.stop()

        async def filter_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.back = 'back'
            self.stop()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_filter_settings(bot), guilds=commands.Greedy[discord.Object])