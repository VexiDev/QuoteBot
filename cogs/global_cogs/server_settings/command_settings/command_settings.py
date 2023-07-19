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
            
            add_settings = self.bot.get_cog("add_command_settings")
            await add_settings.command_add(language_file, interaction, message, settings, main_menu)

        #update the server language setting
        elif command_buttons.page == 'command_edit':
            pass

        #update the server language setting
        elif command_buttons.page == 'command_delete':
            pass

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

            self.add_button = discord.ui.Button(label=self.language_file['command_settings']['mm_buttons']['add'], style=discord.ButtonStyle.green, emoji="<:qbadd:1130279496390553710> ")
            self.add_button.callback = self.command_add
            self.add_item(self.add_button)
            self.edit_button = discord.ui.Button(label=self.language_file['command_settings']['mm_buttons']['edit'], style=discord.ButtonStyle.grey, emoji="<:qbedit:1130279525587103884> ")
            self.edit_button.callback = self.command_edit
            self.add_item(self.edit_button)
            self.delete_button = discord.ui.Button(label=self.language_file['command_settings']['mm_buttons']['delete'], style=discord.ButtonStyle.red, emoji="<:qbdelete:1130279555517653103>")
            self.delete_button.callback = self.command_delete
            self.add_item(self.delete_button)

            self.back_button = discord.ui.Button(label=self.language_file['command_settings']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:info_back:1028918526238523433>", row=2)
            self.back_button.callback = self.command_back
            self.add_item(self.back_button)

        # async def command_buttons(self, interaction: discord.Interaction):
        #     await interaction.response.defer()
        #     self.selection = interaction.data['values'][0] if interaction.data['values'][0] else None
        #     self.stop()

        async def command_add(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'command_add'
            self.stop()

        async def command_edit(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'command_edit'
            self.stop()
            
        async def command_delete(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'command_delete'
            self.stop()

        async def command_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'main_menu'
            self.stop()
            

#------------------EDIT COMMAND------------------


    async def command_edit(self, language_file, interaction, message, settings):
        pass


#------------------DELETE COMMAND------------------
    async def command_delete(self, language_file, interaction, message, settings):
        pass
    


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_command_settings(bot), guilds=commands.Greedy[discord.Object])