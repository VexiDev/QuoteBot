import discord
import datetime
from discord import app_commands
from discord.ext import commands

class server_language_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def language_settings(self, language_file, interaction, message, settings):
        server_settings = self.bot.get_cog('server_settings')

        # create embed
        language_embed = discord.Embed(title=f"{language_file['language_settings']['title']}", description=f"{language_file['language_settings']['description']}", color=0x6eb259)
        language_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        language_embed.timestamp = datetime.datetime.utcnow()
        language_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        language_dropdown = self.language_dropdown(language_file)

        #edit message with dropdown
        await message.edit(embed=language_embed, view=language_dropdown)

        #wait for user to select an option
        await language_dropdown.wait()

        #check if user selected an option
        if language_dropdown.selection == None and language_dropdown.page == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server language setting
        elif language_dropdown.selection != None and language_dropdown.page == None:
            #create loading embed
            loading_embed = discord.Embed(description=f"{language_file['system_messages']['processing_request']}", color=0x068acc)
            #edit message with loading embed
            await message.edit(embed=loading_embed, view=None)
            #update the server language setting
            await server_settings.update_server_settings(interaction.guild_id, "language", f"\'{language_dropdown.selection}\'")
            #---------UPDATE TO NEW LANGUAGE---------
            language = self.bot.get_cog("language")
            #get new server language
            server_language = await language.get_server_language(interaction.guild_id)
            #refresh language setting embed
            language_file = await language.select_language(server_language, "settings_messages.json")
            #inform user of language change
            language_changed_embed = discord.Embed(description=f"**{language_file['language_settings']['language_change_success'][0]}**\n{language_file['language_settings']['language_change_success'][1]}", color=0x068acc)
            await interaction.followup.send(embed=language_changed_embed, ephemeral=True)

        elif language_dropdown.page != None and language_dropdown.selection == None:
            await server_settings.display_settings_page(language_file, interaction, message, settings, language_dropdown.page)
            return

        await self.language_settings(language_file, interaction, message, settings)

    class language_dropdown(discord.ui.View):
        def __init__(self, language_file, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.page = None
            self.language_file = language_file

            languages = [('english', 'en', '🇺🇸'), ('french', 'fr', '🇫🇷'), ('spanish', 'es', '🇪🇸'), ('german', 'de', '🇩🇪')]

            language_options = [discord.SelectOption(
                label=self.language_file['language_settings']['dropdown'][lang_name], 
                value=lang_code, 
                emoji=emoji, 
                default=lang_code == self.language_file['language']
            ) for lang_name, lang_code, emoji in languages]

            self.select = discord.ui.Select(placeholder=self.language_file['language_settings']['dropdown']['dropdown_placeholder'], options=language_options, min_values=1, max_values=1)
            self.select.callback = self.language_dropdown
            self.add_item(self.select)

            self.back_button = discord.ui.Button(label=self.language_file['language_settings']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.language_back
            self.add_item(self.back_button)

        async def language_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = interaction.data['values'][0] if interaction.data['values'][0] else None
            self.stop()

        async def language_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.page = 'main_menu'
            self.stop()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_language_settings(bot), guilds=commands.Greedy[discord.Object])