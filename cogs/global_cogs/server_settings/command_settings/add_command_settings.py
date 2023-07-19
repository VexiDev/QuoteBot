import discord
import traceback
import datetime
import json
import asyncio
from discord import app_commands
import humanize
from discord.ext import commands

class add_command_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def command_add(self, language_file, interaction, message, settings, main_menu, staged_cooldown=None, staged_channels=None, staged_roles=None, applied=False):

        if applied:
            print("getting new settings")
            server_settings = self.bot.get_cog('server_settings')
            settings = await server_settings.get_server_settings(interaction.guild.id)
            applied = False
            #print for debug
            print(f"NEW settings: {settings['add_settings']}")
        print(f"loaded settings: {settings['add_settings']}")
        # define add settings from settings json
        add_cooldown_setting = settings['add_settings']['cooldown']
        add_channel_setting = settings['add_settings']['channels']
        add_role_setting = settings['add_settings']['roles']


        # create description for add settings embed
        description=f"{language_file['command_settings']['add_settings']['description']}"

        if add_cooldown_setting == 0:
            humanized = "Disabled"
        humanized = humanize.naturaldelta(add_cooldown_setting, minimum_unit='seconds')
        description+=f"\n\n**{language_file['command_settings']['add_settings']['field_cooldown']}{humanized}**"

        channel_mentions = ""
        if len(add_channel_setting) == 0:
            channel_mentions = "Disabled"
        else:
            for channels in add_channel_setting:
                channel = interaction.guild.get_channel(int(channels))
                #implement a handler for if a role is None (aka. deleted)
                channel_mentions += f"{channel.mention} "
        description+=f"\n\n**{language_file['command_settings']['add_settings']['field_channel']}{channel_mentions}**"

        role_mentions = ""
        if len(add_role_setting) == 0:
            role_mentions = "Disabled"
        else:
            for roles in add_role_setting:
                role = interaction.guild.get_role(int(roles))
                role_mentions += f"{role.mention} "
        description+=f"\n\n**{language_file['command_settings']['add_settings']['field_role']}{role_mentions}**"

        add_settings_embed = discord.Embed(title=f"{language_file['command_settings']['add_settings']['title']}", description=f"{description}", color=0x6eb259)
        add_settings_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        add_settings_embed.timestamp = datetime.datetime.utcnow()
        add_settings_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        if staged_cooldown != None and staged_channels != None and staged_roles != None:
            print('\nThere are staged settings!')

        add_settings_dropdown = self.add_command_dropdown(self.bot, language_file, settings, staged_cooldown, staged_channels, staged_roles)

        await message.edit(content=None, embed=add_settings_embed, view=add_settings_dropdown)

        await add_settings_dropdown.wait()

        if add_settings_dropdown.channels == None and add_settings_dropdown.roles == None and add_settings_dropdown.cooldown_input == None and add_settings_dropdown.page == None:
            timed_out = main_menu.timed_out(language_file)
            await message.edit(view=timed_out)
            return
        
        elif add_settings_dropdown.page == 'command_settings':
            main_menu = self.bot.get_cog('command_settings')
            await main_menu.command_settings(language_file, interaction, message, settings)
        
        if add_settings_dropdown.channels != None:
            staged_channels = add_settings_dropdown.channels
        
        if add_settings_dropdown.roles != None:
            staged_roles = add_settings_dropdown.roles

        if add_settings_dropdown.cooldown_input != None:
            staged_cooldown = add_settings_dropdown.cooldown_input

        if add_settings_dropdown.applied:
            applied = True

        if applied:
            print('applied')
            await self.command_add(language_file, interaction, message, settings, main_menu, staged_cooldown=None, staged_channels=None, staged_roles=None, applied=True)
        else:
            print('not applied')
            await self.command_add(language_file, interaction, message, settings, main_menu, staged_cooldown, staged_channels, staged_roles, applied)

    class add_command_dropdown(discord.ui.View):
        def __init__(self, bot, language_file, settings, staged_cooldown, staged_channels, staged_roles, timeout=120):
            super().__init__(timeout=timeout)
            self.bot = bot
            self.cooldown_input = staged_cooldown
            self.channels = staged_channels
            self.roles = staged_roles
            self.page = None
            self.language_file = language_file
            self.settings = settings
            self.applied = False

            cooldowns = [("None", 0), ("5sec", 5), ("10sec", 10), ("30sec", 30), ("1min", 60), ("5min", 300), ("10min", 600), ("30min", 1800), ("1hr", 3600), ("6hr", 21600), ("12hr", 43200), ("1day", 86400)]

            cooldown_options = [discord.SelectOption(
                label=self.language_file['command_settings']['add_settings']['cooldown']['dropdown'][f'{cd_label}'], 
                value=cd_value,
                default=True if cd_value == self.cooldown_input else False
            ) for cd_label, cd_value in cooldowns]

            self.cooldown = discord.ui.Select(custom_id="qb-add-settings-cooldown-dropdown",placeholder=self.language_file['command_settings']['add_settings']['cooldown']['placeholder'], options=cooldown_options, min_values=1, max_values=1)
            self.cooldown.callback = self.cooldown_dropdown
            self.add_item(self.cooldown)

            self.channel = discord.ui.ChannelSelect(custom_id="qb-add-settings-channels-dropdown",channel_types=[discord.ChannelType.text], placeholder=self.language_file['command_settings']['add_settings']['channel']['placeholder'], min_values=0, max_values=25, row=2)
            self.channel.callback = self.channel_dropdown
            self.add_item(self.channel)

            self.role = discord.ui.RoleSelect(custom_id="qb-add-settings-roles-dropdown",placeholder=self.language_file['command_settings']['add_settings']['role']['placeholder'], min_values=0, max_values=25, row=3)
            self.role.callback = self.role_dropdown
            self.add_item(self.role)

            self.back_button = discord.ui.Button(label=self.language_file['command_settings']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>", row=4)
            self.back_button.callback = self.add_back
            self.add_item(self.back_button)

            self.apply_button = discord.ui.Button(label=self.language_file['command_settings']['apply_button'], style=discord.ButtonStyle.green, row=4)
            if self.cooldown_input == None and self.channels == None and self.roles == None:
                self.apply_button.disabled = True
            self.apply_button.callback = self.apply_settings
            self.add_item(self.apply_button)

        async def cooldown_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.apply_button.disabled = True
            temp_msg = await interaction.original_response()
            self.cooldown_input = int(interaction.data['values'][0]) if interaction.data['values'][0] else 0
            await temp_msg.edit(view=self)
            self.stop()

        async def channel_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.apply_button.disabled = True
            temp_msg = await interaction.original_response()
            if interaction.data['values'] is not None:
                self.channels = interaction.data['values']
                await temp_msg.edit(view=self)
            else:
                self.channels = []
            self.stop()

        async def role_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            temp_msg = await interaction.original_response()
            self.apply_button.disabled = True
            if interaction.data['values'] is not None:
                self.roles = interaction.data['values']
                await temp_msg.edit(view=self)
            else:
                self.roles = []
            self.stop()

        async def add_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'command_settings'
            self.stop()

        async def apply_settings(self, interaction: discord.Interaction):
            await interaction.response.defer()
            print('apply button pressed')
            self.applied = True
            await self.apply_add_command_update(interaction.guild.id)
            self.stop()

        async def apply_add_command_update(self, guild_id):
            #iterate through the first 3 componenets of interaction.message and store their corresponding values in a list new_settings = {cooldown, channels, roles}
            new_settings = {
                "cooldown": self.cooldown_input,
                "channels": self.channels if self.channels != None else [],
                "roles": self.roles if self.roles != None else []
            }

            print(new_settings)

            #set database variable
            database = self.bot.get_cog("database")
            #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            #create query to get user informtion
            command = f"update guilds set add_settings=\'{json.dumps(new_settings)}\' where guild_id={guild_id}"
            #execute command
            c.execute(command)
            #commit changes to database
            conn.commit()
            #close database connection
            c.close()
            conn.close()

            return
            


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(add_command_settings(bot), guilds = commands.Greedy[discord.Object])
