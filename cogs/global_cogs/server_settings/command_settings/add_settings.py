import discord
from discord import app_commands
from discord.ext import commands
import datetime
from humanize import precisedelta
import asyncio

class add_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def add_command_settings_menu(self, language_file, interaction, message, settings, setting_changed=(False, None)):
        server_settings = self.bot.get_cog('server_settings')
        command_selection_menu = self.bot.get_cog('server_command_settings')

        # get channels from settings
        command_cooldown_raw = settings['add_command_cooldown']
        add_to_self_raw = settings['add_to_self']

        if command_cooldown_raw == 0:
            command_cooldown == "None"
        else:
            command_cooldown = f"{precisedelta(command_cooldown_raw, format='%0.0f')}"
        if add_to_self_raw == True:
            add_to_self = language_file['command_settings']['add_settings']['add_to_self_field_status'][0]
        else:
            add_to_self = language_file['command_settings']['add_settings']['add_to_self_field_status'][1]

        # create embeds
        add_command_settings_alert = discord.Embed(title="", description=f"{language_file['system_messages']['alert_message']}", color=0xff9b21)
       
        description = f"-\n{language_file['command_settings']['add_settings']['cooldown_field']['name']}**{command_cooldown}**\n*{language_file['command_settings']['add_settings']['cooldown_field']['value']}*\n\n{language_file['command_settings']['add_settings']['add_to_self_field']['name']}**{add_to_self}**\n*{language_file['command_settings']['add_settings']['add_to_self_field']['value']}*\n-\n{language_file['command_settings']['add_settings']['description']}"

        add_command_embed = discord.Embed(title=f"{language_file['command_settings']['add_settings']['title']}", description=description, color=0x6eb259)
        
        # add_command_embed.add_field(name=f"{language_file['command_settings']['add_settings']['cooldown_field']['name']}**{command_cooldown}**", value=f"{language_file['command_settings']['add_settings']['cooldown_field']['value']}", inline=False)
        # add_command_embed.add_field(name=f"{language_file['command_settings']['add_settings']['add_to_self_field']['name']}**{add_to_self}**", value=f"{language_file['command_settings']['add_settings']['add_to_self_field']['value']}", inline=False)

        add_command_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        add_command_embed.timestamp = datetime.datetime.utcnow()
        add_command_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        add_command_dropdown = self.add_command_dropdown(language_file, command_cooldown_raw, add_to_self_raw)

        # edit message with dropdown and changed notif if language was changed
        if setting_changed != (False, None):
            add_command_changed_embed = discord.Embed(title="", description=f"{language_file['command_settings']['setting_change_success'][0]} **{setting_changed[1]} {language_file['command_settings']['setting_change_success'][1]}**", color=0x068acc)
            await message.edit(embeds=[add_command_settings_alert, add_command_embed, add_command_changed_embed], view=add_command_dropdown)
        else:
            await message.edit(embeds=[add_command_settings_alert, add_command_embed], view=add_command_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=[add_command_settings_alert, add_command_embed], view=add_command_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await add_command_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if add_command_dropdown.selection == None and add_command_dropdown.back == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server language setting
        elif add_command_dropdown.selection != None and add_command_dropdown.back == None:
            pass

        elif add_command_dropdown.back != None and add_command_dropdown.selection == None:
            await command_selection_menu.command_settings(language_file, interaction, message, settings)
            return

        await self.add_command_settings_menu(language_file, interaction, message, settings)


    class add_command_dropdown(discord.ui.View):
        def __init__(self, language_file, current_cooldown, current_a2s, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.back = None
            self.language_file = language_file
            self.current_cooldown = current_cooldown
            self.current_a2s = current_a2s

            cooldowns = [("None", 0), ("5sec", 5), ("10sec", 10), ("30sec", 30), ("1min", 60), ("5min", 300), ("10min", 600), ("30min", 1800), ("1hr", 3600), ("6hr", 21600), ("12hr", 43200), ("1day", 86400)]

            cooldown_options = [discord.SelectOption(
                label=self.language_file['command_settings']['add_settings']['cooldown']['dropdown'][f'{cd_label}'], 
                value=cd_value,
                default=True if cd_value == self.current_cooldown else False
            ) for cd_label, cd_value in cooldowns]

            add_to_self_options = [
                discord.SelectOption(label=self.language_file['command_settings']['add_settings']['add_to_self']['dropdown']['enabled'], value=True, default=(True if self.current_a2s == True else False)),
                discord.SelectOption(label=self.language_file['command_settings']['add_settings']['add_to_self']['dropdown']['disabled'], value=False, default=(True if self.current_a2s == False else False))
                ]

            self.add_to_self = discord.ui.Select(custom_id="add_command_add_to_self:Add To Self",min_values=1, max_values=1, placeholder=self.language_file['command_settings']['add_settings']['add_to_self']['placeholder'], options=add_to_self_options)
            self.cooldown = discord.ui.Select(custom_id="add_command_cooldown:Command Cooldown",min_values=1, max_values=1, placeholder=self.language_file['command_settings']['add_settings']['cooldown']['placeholder'], options=cooldown_options)
            
            self.cooldown.callback = self.cooldown_dropdown
            self.add_to_self.callback = self.a2s_dropdown
            
            self.add_item(self.cooldown)
            self.add_item(self.add_to_self)

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.add_command_back
            self.add_item(self.back_button)

        async def cooldown_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = (interaction.data['values'][0] if interaction.data['values'] else 0, interaction.data['custom_id'])
            self.stop()

        async def a2s_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = (interaction.data['values'][0] if interaction.data['values'] else True, interaction.data['custom_id'])
            self.stop()

        async def add_command_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.back = 'back'
            self.stop()
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(add_settings(bot), guilds = commands.Greedy[discord.Object])
