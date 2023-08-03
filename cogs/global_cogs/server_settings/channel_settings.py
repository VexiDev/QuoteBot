import discord
from discord import app_commands
from discord.ext import commands
import datetime
import asyncio

class channel_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def channel_settings_menu(self, language_file, interaction, message, settings, channel_changed=(False, None)):
        server_settings = self.bot.get_cog('server_settings')

        # get channels from settings
        added_quotes_channel = interaction.guild.get_channel(settings['added_quotes_channel'])
        logs_channel = interaction.guild.get_channel(settings['action_log_channel'])
        alerts_channel = interaction.guild.get_channel(settings['alerts_channel'])

        if added_quotes_channel != None:
            added_quotes_channel = f"<#{added_quotes_channel.id}>"
        if logs_channel != None:
            logs_channel = f"<#{logs_channel.id}>"
        if alerts_channel != None:
            alerts_channel = f"<#{alerts_channel.id}>"

        # create embeds
        channel_settings_alert = discord.Embed(title="", description=f"{language_file['system_messages']['alert_message']}", color=0xff9b21)
        description = f"{language_file['channel_settings']['description']['header']}\n**{language_file['channel_settings']['description']['quotes_channel']}**{added_quotes_channel}\n**{language_file['channel_settings']['description']['logs_channel']}**{logs_channel}\n**{language_file['channel_settings']['description']['alerts_channel']}**{alerts_channel}\n{language_file['channel_settings']['description']['end']}"
        channel_embed = discord.Embed(title=f"{language_file['channel_settings']['title']}", description=description, color=0x6eb259)
        channel_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        channel_embed.timestamp = datetime.datetime.utcnow()
        channel_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        channel_dropdown = self.channel_dropdown(language_file)

        # edit message with dropdown and changed notif if language was changed
        if channel_changed != (False, None):
            channel_changed_embed = discord.Embed(title="", description=f"{language_file['channel_settings']['channel_change_success'][0]} **{channel_changed[1]} {language_file['channel_settings']['channel_change_success'][1]}**", color=0x068acc)
            await message.edit(embeds=[channel_settings_alert, channel_embed, channel_changed_embed], view=channel_dropdown)
        else:
            await message.edit(embeds=[channel_settings_alert, channel_embed], view=channel_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=[channel_settings_alert, channel_embed], view=channel_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await channel_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if channel_dropdown.selection == None and channel_dropdown.back == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server language setting
        elif channel_dropdown.selection != None and channel_dropdown.back == None:

            #get the updated channel db key and embed name
            updated_channel = channel_dropdown.selection[1].split(":")
            updated_channel_id = channel_dropdown.selection[0]
            updated_channel_key = updated_channel[0].replace("_button", "")
            updated_channel_name = updated_channel[1]

            #update the corresponding channel setting
            await server_settings.update_server_settings(interaction.guild_id, updated_channel_key, updated_channel_id)
            
            settings = await server_settings.get_server_settings(interaction.guild_id)

            # reload the menu and inform user of language change
            await self.channel_settings_menu(language_file, interaction, message, settings, channel_changed=(True, updated_channel_name))
            return

        elif channel_dropdown.back != None and channel_dropdown.selection == None:
            await server_settings.settings_main_menu(language_file, interaction, message, settings)
            return

        await self.channel_settings_menu(language_file, interaction, message, settings)

    class channel_dropdown(discord.ui.View):
        def __init__(self, language_file, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.back = None
            self.language_file = language_file


            self.added_quotes = discord.ui.ChannelSelect(custom_id="added_quotes_channel:Added Quotes Channel", min_values=0, max_values=1, channel_types=[discord.ChannelType.text], placeholder=self.language_file['channel_settings']['placeholders']['added_quotes'])
            self.logs = discord.ui.ChannelSelect(custom_id="action_log_channel:Log Channel", min_values=0, max_values=1, channel_types=[discord.ChannelType.text], placeholder=self.language_file['channel_settings']['placeholders']['logs'])
            self.alerts = discord.ui.ChannelSelect(custom_id="alerts_channel:Mod Alerts Channel", min_values=0, max_values=1, channel_types=[discord.ChannelType.text], placeholder=self.language_file['channel_settings']['placeholders']['alerts'])
            
            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>", row=4)
            self.clear_added_selection = discord.ui.Button(label="Unset Added",custom_id="added_quotes_channel_button:Added Quotes Channel",style=discord.ButtonStyle.red,row=4)
            self.clear_logs_selection = discord.ui.Button(label="Unset Logs",custom_id="action_log_channel_button:Log Channel",style=discord.ButtonStyle.red,row=4)
            self.clear_alerts_selection = discord.ui.Button(label="Unset Alerts",custom_id="alerts_channel_button:Mod Alerts Channel",style=discord.ButtonStyle.red, row=4)


            self.added_quotes.callback = self.channel_dropdowns
            self.logs.callback = self.channel_dropdowns
            self.alerts.callback = self.channel_dropdowns
            self.back_button.callback = self.channel_back
            self.clear_added_selection.callback = self.clear_selection
            self.clear_logs_selection.callback = self.clear_selection
            self.clear_alerts_selection.callback = self.clear_selection
            
            self.add_item(self.back_button)
            self.add_item(self.added_quotes)
            self.add_item(self.logs)
            self.add_item(self.alerts)
            self.add_item(self.clear_added_selection)
            self.add_item(self.clear_logs_selection)
            self.add_item(self.clear_alerts_selection)
            

        async def channel_dropdowns(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = (interaction.data['values'][0] if interaction.data['values'] else -1, interaction.data['custom_id'])
            self.stop()

        async def channel_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.back = 'back'
            self.stop()

        async def clear_selection(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = (-1, interaction.data['custom_id'])
            self.stop()
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(channel_settings(bot), guilds = commands.Greedy[discord.Object])
