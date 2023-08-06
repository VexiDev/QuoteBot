import discord
from discord import app_commands
import datetime
from discord.ext import commands

class server_automod_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def automod_settings(self, language_file, interaction, message, settings):
        main_menu = self.bot.get_cog('server_settings')
        automod_actions_settings = self.bot.get_cog('automod_actions')

        # create embed
        if settings['filter_detection_types'] != []:
            automod_embed = discord.Embed(title=f"{language_file['automod_settings']['title']}", description=f"{language_file['automod_settings']['description']}", color=0x6eb259)
        else:
            automod_embed = discord.Embed(title=f"{language_file['automod_settings']['title']}", description=f"{language_file['automod_settings']['no_detections_enabled'][1]}", color=0x6eb259)
        automod_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        automod_embed.timestamp = datetime.datetime.utcnow()
        automod_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        automod_select = self.automod_select(language_file, settings['filter_detection_types'])
        


        if settings['filter_detection_types'] == []:
            # no embed warning
            no_detections_embed = discord.Embed(title="", description=f"{language_file['automod_settings']['no_detections_enabled'][0]}", color=0xff9b21)
            #edit message with dropdown
            await message.edit(embeds=[no_detections_embed, automod_embed], view=automod_select)
        else:
            #edit message with dropdown
            await message.edit(embed=automod_embed, view=automod_select)

        #wait for user to select an option
        await automod_select.wait()

        #check if user selected an option
        if automod_select.page == None:
            #time out the message
            timed_out = main_menu.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        elif automod_select.page == "main_menu":
            await main_menu.display_settings_page(language_file, interaction, message, settings, automod_select.page)
            return

        elif automod_select.page == "filter_settings":
            filter_page = self.bot.get_cog('server_filter_settings')
            await filter_page.filter_settings(language_file, interaction, message, settings)
        
        elif automod_select.page != None and automod_select.page != "main_menu":
            await automod_actions_settings.automod_actions(language_file, interaction, message, settings, automod_select.page)
            return

        await self.automod_settings(language_file, interaction, message, settings)


    class automod_select(discord.ui.View):
        def __init__(self, language_file, current_detections, timeout=120):
            super().__init__(timeout=timeout)
            self.page = None
            self.language_file = language_file
            self.current_detections = current_detections


            if self.current_detections != []:
                automod_select_options = [discord.SelectOption(
                    label=self.language_file['automod_settings']['dropdown'][amd_type]['label'], 
                    description=self.language_file['automod_settings']['dropdown'][amd_type]['desc'],
                    value=f'{amd_type}',
                ) for amd_type in current_detections]


                self.automod_select = discord.ui.Select(custom_id="automod_select", placeholder=self.language_file['automod_settings']['dropdown']['placeholder'], options=automod_select_options, min_values=1, max_values=1)

                self.automod_select.callback = self.automod_selection

                self.add_item(self.automod_select)
            else:
                self.no_detections_enabled = discord.ui.Button(label=self.language_file['automod_settings']['no_detections_enabled'][2], style=discord.ButtonStyle.green, row=1)
                self.no_detections_enabled.callback = self.filter_settings
                self.add_item(self.no_detections_enabled)

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:info_back:1028918526238523433>", row=2)
            self.back_button.callback = self.automod_back
            self.add_item(self.back_button)

        async def automod_selection(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = interaction.data['values'][0] if interaction.data['values'] else "main_menu"
            self.stop()

        async def filter_settings(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = "filter_settings"
            self.stop()

        async def automod_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'main_menu'
            self.stop()
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_automod_settings(bot), guilds=commands.Greedy[discord.Object])