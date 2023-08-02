import discord
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands

class server_language_settings(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def language_settings(self, language_file, interaction, message, settings, language_changed=False):
        server_settings = self.bot.get_cog('server_settings')

        # create embed
        language_embed = discord.Embed(title=f"{language_file['language_settings']['title']}", description=f"{language_file['language_settings']['description']}", color=0x6eb259)
        language_embed.set_author(name=f"{interaction.guild.name}", icon_url=interaction.guild.icon.url)
        language_embed.timestamp = datetime.datetime.utcnow()
        language_embed.set_footer(text=f"{language_file['system_messages']['embed_footer']}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")

        #create dropdown
        language_dropdown = self.language_dropdown(language_file)

        # edit message with dropdown and changed notif if language was changed
        if language_changed:
            language_changed_embed = discord.Embed(title="", description=f"**{language_file['language_settings']['language_change_success']}**", color=0x068acc)
            await message.edit(embeds=[language_changed_embed, language_embed], view=language_dropdown)
        else:
            await message.edit(embed=language_embed, view=language_dropdown)

        # Create a task that can be cancelled later
        async def remove_embed_after_delay():
            await asyncio.sleep(5)
            await message.edit(embeds=[language_embed], view=language_dropdown)

        # Create the task
        task = asyncio.create_task(remove_embed_after_delay())

        # Wait for user to select an option
        await language_dropdown.wait()

        # If the user has selected an option/button, cancel the task
        task.cancel()

        try:
            # Await the task to handle the cancellation properly
            await task
        except asyncio.CancelledError:
            # This error is expected, task has been cancelled
            pass

        #check if user selected an option
        if language_dropdown.selection == None and language_dropdown.back == None:
            #time out the message
            timed_out = server_settings.timed_out(language_file)
            await message.edit(view=timed_out)
            return

        #update the server language setting
        elif language_dropdown.selection != None and language_dropdown.back == None:

            
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
            #update message language and inform user of language change
            await self.language_settings(language_file, interaction, message, settings, language_changed=True)
            return

        elif language_dropdown.back != None and language_dropdown.selection == None:
            await server_settings.settings_main_menu(language_file, interaction, message, settings)
            return

        await self.language_settings(language_file, interaction, message, settings, language_changed=False)

    class language_dropdown(discord.ui.View):
        def __init__(self, language_file, timeout=120):
            super().__init__(timeout=timeout)
            self.selection = None
            self.back = None
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

            self.back_button = discord.ui.Button(label=self.language_file['system_messages']['back_button'], style=discord.ButtonStyle.blurple, emoji="<:help_back:1028918526238523433>")
            self.back_button.callback = self.language_back
            self.add_item(self.back_button)

        async def language_dropdown(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.selection = interaction.data['values'][0] if interaction.data['values'][0] else None
            self.stop()

        async def language_back(self, interaction: discord.Interaction):
            await interaction.response.defer()
            self.back = 'back'
            self.stop()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_language_settings(bot), guilds=commands.Greedy[discord.Object])