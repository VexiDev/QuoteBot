import discord
from discord import app_commands
import datetime
from discord.ext import commands

class server_command_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def command_settings(self, language_file, interaction, message, settings):
        main_menu = self.bot.get_cog('server_settings')

        # create embed
        command_embed = discord.Embed(title=f"{language_file['command_settings']['title']}", description=f"{language_file['command_settings']['description']}", color=0x6eb259)
        command_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        command_embed.timestamp = datetime.datetime.utcnow()
        command_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        command_buttons = self.command_buttons(language_file)

        #edit message with dropdown
        await message.edit(embed=command_embed, view=command_buttons)

        #wait for user to select an option
        await command_buttons.wait()

        #check if user selected an option
        if command_buttons.page == None:
            #time out the message
            timed_out = main_menu.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server language setting
        elif command_buttons.page == 'command_add':
            
            add_settings = self.bot.get_cog("add_settings")
            await add_settings.add_command_settings_menu(language_file, interaction, message, settings)
            return

        #update the server language setting
        elif command_buttons.page == 'command_edit':
            
            edit_settings = self.bot.get_cog("edit_settings")
            await edit_settings.edit_command_settings_menu(language_file, interaction, message, settings)
            return

        #update the server language setting
        elif command_buttons.page == 'command_delete':

            delete_settings = self.bot.get_cog("delete_settings")
            await delete_settings.delete_command_settings_menu(language_file, interaction, message, settings)
            return

        #update the server language setting
        elif command_buttons.page == 'command_profile':
            
            profile_settings = self.bot.get_cog("profile_settings")
            await profile_settings.profile_command_settings_menu(language_file, interaction, message, settings)
            return

        elif command_buttons.page != None:
            await main_menu.display_settings_page(language_file, interaction, message, settings, command_buttons.page)
            return

        await self.command_settings(language_file, interaction, message, settings)


    class command_buttons(discord.ui.View):
        def __init__(self, language_file, timeout=120):
            super().__init__(timeout=timeout)
            self.page = None
            self.language_file = language_file

            # self.select = discord.ui.Select(placeholder=self.language_file['command_settings']['dropdown']['dropdown_placeholder'], options=language_options, min_values=1, max_values=1)
            # self.select.callback = self.command_buttons
            # self.add_item(self.select)

            command_select_options = [discord.SelectOption( label=self.language_file['command_settings']['dropdown']['add'], value="command_add",emoji="<:qbadd:1130279496390553710>"),
            discord.SelectOption(label=self.language_file['command_settings']['dropdown']['delete'],value="command_delete",emoji="<:qbdelete:1130279555517653103>"),
            discord.SelectOption(label=self.language_file['command_settings']['dropdown']['edit'],value="command_edit",emoji="<:qbedit:1130279525587103884>"),
            discord.SelectOption(label=self.language_file['command_settings']['dropdown']['profile'],value="command_profile",emoji="<:profile:1030032830891311174>")
            ]

            self.command_select = discord.ui.Select(custom_id="command_select", placeholder=self.language_file['command_settings']['dropdown']['placeholder'], options=command_select_options, min_values=1, max_values=1)

            self.command_select.callback = self.command_selection

            self.add_item(self.command_select)

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:info_back:1028918526238523433>", row=2)
            self.back_button.callback = self.command_back
            self.add_item(self.back_button)

        async def command_selection(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = interaction.data['values'][0] if interaction.data['values'] else "main_menu"
            self.stop()

        async def command_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'main_menu'
            self.stop()
            

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_command_settings(bot), guilds=commands.Greedy[discord.Object])