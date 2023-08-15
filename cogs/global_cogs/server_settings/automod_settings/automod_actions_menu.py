import discord
from discord import app_commands
import datetime
import asyncio
from discord.ext import commands

class automod_actions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def automod_actions(self, language_file, interaction, message, settings, detection_type, actions_changed=(False, None)):
        server_settings = self.bot.get_cog('server_settings')
        actions_main_menu = self.bot.get_cog('server_automod_settings')

        # create embed
        actions_embed = discord.Embed(title=f"{language_file['automod_settings']['dropdown'][f'{detection_type}']['label']} {language_file['automod_actions']['title']}", description=f"{language_file['automod_actions']['description']['header']}\n-", color=0x6eb259)
        actions_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        actions_embed.timestamp = datetime.datetime.utcnow()
        actions_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        
        if settings[f'automod_{detection_type}_actions'] == []:
            actions_embed.add_field(name=f"{language_file['automod_actions']['description']['no_actions']}", value=f"{language_file['automod_actions']['description']['no_actions']['desc']}", inline=False)
        else:
            for action in settings[f'automod_{detection_type}_actions']:
                value = language_file['automod_actions']['dropdown'][action]['desc'] + " " + language_file['automod_actions']['dropdown'][action]['example']
                actions_embed.add_field(name=f"{language_file['automod_actions']['dropdown'][action]['label']}", value=f"*{value}*", inline=False)
        
        actions_embed.add_field(name=f"-", value=f"{language_file['automod_actions']['description']['end']}", inline=False)

        #get current actions
        current_actions = settings[f'automod_{detection_type}_actions']
        
        embed_list = [actions_embed]

        if settings['alerts_channel'] == -1:
            embed_list = [discord.Embed(title="", description=f"{language_file['automod_actions']['no_alerts_channel']}", color=0xff9b21)] + embed_list
            #create dropdown
            actions_dropdown = self.actions_dropdown(language_file, detection_type, current_actions, jump_button=True)
        else:
            #create dropdown
            actions_dropdown = self.actions_dropdown(language_file, detection_type, current_actions, jump_button=False)

        # edit message with dropdown and changed notif if filter was changed
        if actions_changed != (False, None):
            actions_changed_embed = discord.Embed(title="", description=f"**{language_file['automod_actions']['action_change_success']}**", color=0x068acc)
            # create a new list with all the elements of embed_list and the new element
            changes_embed_list = embed_list + [actions_changed_embed]
            # pass the new_embed_list to the embeds parameter
            await message.edit(embeds=changes_embed_list, view=actions_dropdown)
        else:
            await message.edit(embeds=embed_list, view=actions_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=embed_list, view=actions_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await actions_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if actions_dropdown.page == None and actions_dropdown.selection == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return
        
        elif actions_dropdown.selection != None and actions_dropdown.page == None:

            #check if a alerts channel is set, if not send a new response with a warning and a hotlink button to the channel settings
            # if settings['alerts_channel'] == -1 and ("Hold" in actions_dropdown.selection[0] or "Notify" in actions_dropdown.selection[0]):
            #     print('sending followup')
                
            #     hotbutton = self.channel_settings_button(language_file)
            #     hotbutton_embed = discord.Embed(title="", description=f"{language_file['automod_actions']['no_alerts_channel']}", color=0xff9b21)
            #     no_alerts_channel_message = await interaction.followup.send(embed=hotbutton_embed, view=hotbutton, ephemeral=True)
            #     print('sent')
            #     #wait for user to press the button
            #     await hotbutton.wait()
            #     if hotbutton.pressed == True:
            #         channel_settings = self.bot.get_cog('channel_settings')
            #         await channel_settings.channel_settings_menu(language_file, interaction, message, settings)
            #         return
            #     else:
            #         timed_out = server_settings.timed_out(language_file)
            #         await no_alerts_channel_message.edit(view=timed_out)
            #         return

            print(actions_dropdown.selection[0])
            
            #prepare list for postegres
            type_list = '{' + ', '.join(f'"{item}"' for item in actions_dropdown.selection[0]) + '}'

            #update the actions for the selected detection type
            await server_settings.update_server_settings(interaction.guild_id, f"automod_{actions_dropdown.selection[1]}_actions", f"\'{type_list}\'")

            settings = await server_settings.get_server_settings(interaction.guild_id)

            await self.automod_actions(language_file, interaction, message, settings, detection_type, actions_changed=(True, ""))
            return
        
        elif actions_dropdown.page == "actions_main_menu":
            await actions_main_menu.automod_settings(language_file, interaction, message, settings)
            return
        
        elif actions_dropdown.page == "channel_settings":

            channel_settings = self.bot.get_cog('channel_settings')
            await channel_settings.channel_settings_menu(language_file, interaction, message, settings)
            return

        await self.automod_actions(language_file, interaction, message, settings, detection_type)

    class actions_dropdown(discord.ui.View):
        def __init__(self, language_file, detection, current_actions, jump_button, timeout=120):
            super().__init__(timeout=timeout)
            self.page = None
            self.selection = None
            self.language_file = language_file
            self.detection = detection
            self.current_actions = current_actions
            self.jump_button = jump_button

            automod_detections = ['Warn', 'Notify', 'Hold', 'Cancel']

            actions_dropdown_options = [discord.SelectOption(
                label=self.language_file['automod_actions']['dropdown'][amd_type]['label'], 
                description=self.language_file['automod_actions']['dropdown'][amd_type]['desc'],
                value=f'{amd_type}',
                default=True if amd_type in current_actions else False
            ) for amd_type in automod_detections]


            self.actions_dropdown = discord.ui.Select(custom_id=f"{self.detection}", placeholder=self.language_file['automod_actions']['dropdown']['placeholder'], options=actions_dropdown_options, min_values=0, max_values=4)
            self.jumpbutton = discord.ui.Button(label=f"{self.language_file['automod_actions']['jump_to_channel_settings_button']}", style=discord.ButtonStyle.red, row=2)
            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:info_back:1028918526238523433>", row=2)
            
            self.actions_dropdown.callback = self.select_actions_dropdown
            self.back_button.callback = self.automod_back
            self.jumpbutton.callback = self.jump_to_channel_settings
            
            self.add_item(self.actions_dropdown)
            self.add_item(self.back_button)
            
            if self.jump_button == True:
                self.add_item(self.jumpbutton)

        async def jump_to_channel_settings(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = "channel_settings"
            self.stop()

        async def select_actions_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            message = await interaction.original_response()
            loading_embed = discord.Embed(description=f"{self.language_file['system_messages']['processing_request']}", color=0x068acc)

            # Keep only the first 2 embeds
            message.embeds = message.embeds[:2]

            message.embeds.append(loading_embed)

            # Make sure to edit the message to actually display the new embed
            await message.edit(embeds=message.embeds, view=None)
            self.selection = (interaction.data['values'], interaction.data['custom_id']) if interaction.data['values'] else ([], interaction.data['custom_id'])
            self.stop()

        async def automod_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'actions_main_menu'
            self.stop()
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(automod_actions(bot), guilds=commands.Greedy[discord.Object])