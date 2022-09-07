import discord as disc
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands


class action_manager(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def nsfw_actions(self, interaction, message, user, nsfw, quote, filter_result):
        # >> RETURN FORMAT (NSFW, REVIEW, CANCEL, REASON) <<

        if filter_result[0]:
            nsfw = True
        if filter_result[1]:
            #send quote to review channel
            #TO BE IMPLEMENTED
            pass
        if filter_result[2]:
            #send console alert
            print(f"\nWARNING: a quote has been blocked by QuoteBot\nQuote: {quote}\nReason: {filter_result[3]}\nGuild: {interaction.guild.id}\nUser:{interaction.user.id}")
            #create blocked embed
            blocked_embed = disc.Embed(title="**Your quote was blocked by our content filter!**",description="If your quote includes any of the following it will get blocked:\n- Links of any kind\n- Personal information (email, ip, ssn, etc)",  color=0xff0000)
            #set alert as the thumbnail
            blocked_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/916091272186454076/1016819694843469865/alert.png")
            #create footer with USERID
            blocked_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1016824630004158506/logol.png")
            #set timestamp to discord time
            blocked_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=blocked_embed, view=None)
            try:
                #after timeout delete the message
                await message.delete(delay=30)
                return "blocked"
            except:
                #if it fails means it was hidden therefore we ignore
                pass
        
        return nsfw

    async def blacklist_actions(self, interaction, message, database):
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select * from users where uid={interaction.user.id}"
        #execute command
        c.execute(command)
        #get results of query
        results=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        #check if user is blacklisted
        if results[0][3]:
            #send console alert
            print(f"\nWARNING: a blacklisted user has attempted to use quotebot\nUser: {interaction.user.id}\nReason: {results[0][7]}\nGuild: {interaction.guild.id}")
            #create blocked embed
            blacklisted_embed = disc.Embed(title="**User Blacklisted**",description=f"Your account has been blacklisted from using QuoteBot.\n\nReason: {results[0][7]}\n\n*If you feel this blacklist is unfair you can open an appeal ticket in the support discord*",  color=0xff0000)
            #set blocked emoji as the thumbnail
            blacklisted_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/916091272186454076/1016829340576661534/block.png")
            #create footer with USERID
            blacklisted_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1016824630004158506/logol.png")
            #set timestamp to discord time
            blacklisted_embed.timestamp = datetime.datetime.utcnow()
            await message.edit(embed=blacklisted_embed, view=None)

            try:
                #after timeout delete the message
                await message.delete(delay=30)
                return "blacklisted"
            except:
                #if it fails means it was hidden therefore we ignore
                pass
        
        return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(action_manager(bot), guilds = commands.Greedy[disc.Object])
