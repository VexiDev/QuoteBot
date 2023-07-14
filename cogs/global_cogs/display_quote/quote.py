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

    async def quote(self, interaction: discord.Interaction, user: discord.User, quote="None", temp=False):
        try: 
            #--------LOADING MENU---------
            #Create loading embed for profile
            loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
            #Send loading message
            await interaction.response.defer()
            #assign message for future edits
            message = await interaction.followup.send(embed=loading_embed)

            
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
            #check user blacklist
            status = await action_manager.user_blacklist_actions(interaction, message, database)
            if status == "user_blacklisted":
                return
            #check target blacklist
            status = await action_manager.target_blacklist_actions(interaction, user, message, database)
            if status == "target_blacklisted":
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
            #create query for all quotes
            if quote == "None":
                command = f"select * from quotes where uid={user.id} and guild_id={interaction.guild.id} and hidden=false"
            else:
                command = f"select * from quotes where uid={user.id} and guild_id={interaction.guild.id} and hidden=false and lower(quote) like lower('%{quote}%')"
            #execute command
            c.execute(command)
            #get results of query
            results=c.fetchall()
            #close database connection
            c.close()
            conn.close()

            #randomly select a quote
            if len(results) > 0:
                randquote = choice(results)
            else:
                randquote = None

            if randquote != None:
                if len(randquote[3]) == 10:
                    quote_date = datetime.datetime.strptime(randquote[3], "%d/%m/%Y").strftime("%d/%m/%Y")
                elif len(randquote[3]) == 19:
                    quote_date = datetime.datetime.strptime(randquote[3], "%d/%m/%Y %H:%M:%S").strftime("%d/%m/%Y")
                else:
                    pass
                #create quote embed
                random_quote_embed = discord.Embed(title=f"\"{randquote[2]}\"", color=0x4381C1)
                #Create fake quote author for confirm
                random_quote_embed.set_author(name=f"{user.display_name} - {quote_date}", icon_url=user.display_avatar.url)
            else:
                #create no quote found embed
                random_quote_embed = discord.Embed(title=f"Could not find a matching quote!", description="Make sure everything is spelled correctly!\n\u200B", color=0xDF3B57)
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
