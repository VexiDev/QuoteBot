import discord
import asyncio
from random import *
import datetime
import traceback as trace
from discord import app_commands
from discord.ext import commands

class quote(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def quote(self, interaction: discord.Interaction, user: discord.User, temp=False):
        try: 
            #--------LOADING MENU---------
            #Create loading embed for profile
            loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
            #Send loading message
            await interaction.response.send_message(embed=loading_embed)
            #assign message for future edits
            message = await interaction.original_response()
            
            #set database variable
            database = self.bot.get_cog("database")
            
            #------Pass System Checks-----
            #import system checks cog
            action_manager = self.bot.get_cog("action_manager")
            profile_manager = self.bot.get_cog("profile_creator")
            #check maintenance
            #check channel restrictions
            #check if profile exist for both user and target
            await profile_manager.creator(interaction.user)
            await profile_manager.creator(user)
            #check blacklist
            status = await action_manager.blacklist_actions(interaction, message, database)
            if status == "blacklisted":
                return
            #check if user is a bot
            if user.bot or interaction.user.bot:
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

            #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            #create query for all non nsfw quotes
            command = f"select * from quotes where uid={user.id} and guild_id={interaction.guild.id} and hidden=false"
            #execute command
            c.execute(command)
            #get results of query
            results=c.fetchall()
            #close database connection
            c.close()
            conn.close()

            #randomly select a quote
            if len(results) > 0:
                randquote = choice(results)[2]
            else:
                randquote = None

            if randquote != None:
                #create quote embed
                random_quote_embed = discord.Embed(title=f"\"{randquote}\"", color=0x4381C1)
                #Create fake quote author for confirm
                random_quote_embed.set_author(name=user, icon_url=user.display_avatar.url)
            else:
                #create no quote found embed
                random_quote_embed = discord.Embed(title=f"{user} has no quotes!", description="-\nAdd some with **/add**!\n\u200B", color=0xDF3B57)
            #CREATE PAGE FOOTER
            #create footer with USERID
            random_quote_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            random_quote_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=random_quote_embed)
            if temp==True:
                try:
                    #after timeout delete the message
                    await message.delete(delay=120)
                    return
                except:
                    #if it fails means it was hidden therefore we ignore
                    pass
        except:
            trace.print_exc()



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(quote(bot), guilds = commands.Greedy[discord.Object])
