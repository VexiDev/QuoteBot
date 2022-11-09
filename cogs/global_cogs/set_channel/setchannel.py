import discord
import datetime
import traceback as trace
from discord import app_commands
from discord.ext import commands

class setchannel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def channel_set(self, interaction, type, channel):
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
        #import system check cogs
        content_filter = self.bot.get_cog("content_filter")
        action_manager = self.bot.get_cog("action_manager")
        profile_manager = self.bot.get_cog("profile_creator")
        #check maintenance

        #check blacklist
        status = await action_manager.blacklist_actions(interaction, message, database)
        if status == "blacklisted":
            return

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

        #-----CHECK FOR DUPLICATE-----
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select * from channels where guild_id={interaction.guild.id} and type='{type}'"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()
                
        if len(results) == 1:
            #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            #update new channel
            command = f"update channels set channel_id={channel.id} where guild_id={interaction.guild.id} and type='{type}'"
            #execute command
            c.execute(command)
            #close database connection
            conn.commit()
            c.close()
            conn.close()
            update_embed = discord.Embed(description=f"<:yes:892537190347837450> **Channel Successfully Updated**\n\nChannel <#{channel.id}> is now the **{type}** channel", color=0x8AEA92)
            update_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            update_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=update_embed)

            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass
        elif len(results) == 0:
             #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            #insert new channel
            command = f"insert into channels(guild_id, channel_id, type) values({interaction.guild.id}, {channel.id}, '{type}')"
            #execute command
            c.execute(command)
            #close database connection
            conn.commit()
            c.close()
            conn.close()
            force_update_embed = discord.Embed(description=f"<:yes:892537190347837450> **Channel Successfully Updated**\n\nChannel <#{channel.id}> is now the **{type}** channel", color=0x8AEA92)
            force_update_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            force_update_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=force_update_embed)
            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

        elif len(results) > 1:
            #connect to database
            conn = database.connect()
            #set database cursor
            c = conn.cursor()
            #delete all existing channels of that type from the guild
            command = f"delete from channels where guild_id={interaction.guild.id} and type='{type}'"
            #execute command
            c.execute(command)
            #insert new channel
            command = f"insert into channels(guild_id, channel_id, type) values({interaction.guild.id}, {channel.id}, '{type}')"
            #execute command
            c.execute(command)
            #close database connection
            conn.commit()
            c.close()
            conn.close()
            force_update_embed = discord.Embed(description=f"<:yes:892537190347837450> **Channel Successfully Updated**\n\nChannel <#{channel.id}> is now the **{type}** channel", color=0x8AEA92)
            force_update_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            force_update_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=force_update_embed)
            try:
                #after timeout delete the message
                await message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(setchannel(bot), guilds = commands.Greedy[discord.Object])
