import discord
import datetime
from discord import app_commands
from discord.ext import commands

class edit_bio(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    async def bio(self, interaction: discord.Interaction, bio="", hidden=False):
        #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
        #Send loading message
        await interaction.response.defer(ephemeral=hidden)
        #assign message for future edits
        message = await interaction.followup.send(embed=loading_embed)

        #set database variable
        database = self.bot.get_cog("database")

        #------Pass System Checks-----
        #import system checks cog
        content_filter = self.bot.get_cog("content_filter")
        action_manager = self.bot.get_cog("action_manager")
        profile_manager = self.bot.get_cog("profile_creator")
        #check maintenance
        #check channel restrictions
        #check if profile exist for user 
        await profile_manager.creator(interaction.user)

        #check if user is a bot
        if interaction.user.bot:
            #if is a bot cancel request
            is_bot_embed = discord.Embed(title="Bots cannot use QuoteBot", color=0xe02f2f)
            await message.edit(embed=is_bot_embed)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

        #check user blacklist
        user_status = await action_manager.user_blacklist_actions(interaction, message, database)
        if user_status == "user_blacklisted":
            return

        #default nsfw to false
        nsfw = False
        #send bio to filter api
        filter_result = await content_filter.check_nsfw(bio, type="bio")
        #take action based on results
        nsfw = await action_manager.nsfw_actions(interaction, message, interaction.user, nsfw, bio, filter_result, type="bio")
        #if action manager blocks the quote end add function
        if nsfw == "blocked":
            return


        #-----CHECK FOR EXIST-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query to get user informtion
        command = f"select * from users where uid={interaction.user.id}"
        #execute command
        c.execute(command)
        #get results of query
        userinfo=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        #check if the bio is the same
        if bio == userinfo[0][8]:

                #SEND ALREADY EXIST
                duplicate_embed = discord.Embed(title="This is already your bio", color=0xffb300)
                #Create fake quote author for confirm
                duplicate_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                #CREATE PAGE FOOTER
                #create footer with USERID
                duplicate_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
                #set timestamp to discord time
                duplicate_embed.timestamp = datetime.datetime.utcnow()
                            
                await interaction.followup.send(embed=duplicate_embed, ephemeral=True)
                await message.delete()
                return


        verify_embed = discord.Embed(title=f"\n{bio}\n", description=f"-\n*Please confirm that the text above is correct*", color=0xffb300)
        #Create fake quote author for confirm
        verify_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
        #CREATE PAGE FOOTER
        #create footer with USERID
        verify_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        #set timestamp to discord time
        verify_embed.timestamp = datetime.datetime.utcnow()
        confirm_buttons = self.Confirm()
        await message.edit(embed=verify_embed, view=confirm_buttons)

        await confirm_buttons.wait()
        if confirm_buttons.value is None:
            #if timed out delete message
            await message.delete()
            #if timed out place warning in console
            print(f'WARNING: confirm_buttons() view in server {interaction.guild.id} has timed out')
        elif confirm_buttons.value:
            confirm_embed = discord.Embed(title="Please wait while we update your bio", description="<a:loading:892534287415525386> Processing request", color=0x068acc)
            #CREATE PAGE FOOTER
            #create footer with USERID
            confirm_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            confirm_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=confirm_embed, view=None)
            #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            command = f"update users set bio='{bio}' where uid={interaction.user.id}"
            #execute command
            c.execute(command)
            #commit all changes
            conn.commit()
            #close database connection
            c.close()
            conn.close()

            #send complete message
            complete_embed = discord.Embed(title="Your bio has been updated", color=0xffb300)
            #Add user as author
            complete_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
            #CREATE PAGE FOOTER
            #create footer with USERID
            complete_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            complete_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=complete_embed, view=None)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

        else:
            #create canceled embed
            canceled_embed = discord.Embed(description="<:no:907768020561190983> **Canceled**",  color=0xff0000)
            
            await interaction.followup.send(embed=canceled_embed, ephemeral=True)
            await message.delete()
            return


    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None


        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji="<:yes:892537190347837450>")
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.value = True
            self.stop()

        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji="<:no:907768020561190983>")
        async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.value = False
            self.stop()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(edit_bio(bot), guilds = commands.Greedy[discord.Object])
