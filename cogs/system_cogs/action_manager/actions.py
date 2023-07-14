import discord as disc
import datetime
import asyncio
from discord import app_commands
from discord.ext import commands


class action_manager(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def nsfw_actions(self, interaction, message, user, nsfw, quote, filter_result, type="quote"):
        # >> RETURN FORMAT (NSFW, REVIEW, CANCEL, REASON) <<

        if filter_result[0]:
            nsfw = True
            if type == "bio":
                #send console alert
                print(f"\nWARNING! A bio has been blocked by QuoteBot:\n  bio: {quote}\n  Reason: {filter_result[3]}\n  Guild: {interaction.guild.id}\n  User: {interaction.user.id}")
                #create blocked embed
                blocked_embed = disc.Embed(title="**Your new bio was blocked by our content filter!**",description="If your bio includes any of the following it will get blocked:If your bio includes any of the following it will get blocked:\n- Sexual Harassment\n- Discriminatory Terms\n- Derogatory Terms\n- Sensitive Topics\n- Links of any kind\n- Personal information (email, ip, etc)",  color=0xff0000)

        if filter_result[1]:
            #send quote to review channel
            #TO BE IMPLEMENTED
            pass
        if filter_result[2]:
            if type == "quote":
                #send console alert
                print(f"\nWARNING! A quote has been blocked by QuoteBot:\n  Quote: {quote}\n  Reason: {filter_result[3]}\n  Guild: {interaction.guild.id}\n  User: {interaction.user.id}")
                #create blocked embed
                blocked_embed = disc.Embed(title="**Your quote was blocked by our content filter!**",description="If your quote includes any of the following it will get blocked:\n- Links of any kind\n- Personal information (email, ip, etc)",  color=0xff0000)
            elif type == "bio":
                #send console alert
                print(f"\nWARNING! A bio has been blocked by QuoteBot:\n  bio: {quote}\n  Reason: {filter_result[3]}\n  Guild: {interaction.guild.id}\n  User: {interaction.user.id}")
                #create blocked embed
                blocked_embed = disc.Embed(title="**Your new bio was blocked by our content filter!**",description="If your bio includes any of the following it will get blocked:\n- Sexual Harassment\n- Discriminatory Terms\n- Derogatory Terms\n- Sensitive Topics\n- Links of any kind\n- Personal information (email, ip, etc)",  color=0xff0000)

            #set alert as the thumbnail
            blocked_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/916091272186454076/1016819694843469865/alert.png")
            #create footer with USERID
            blocked_embed.set_footer(text=f"QuoteBot | ID: {interaction.user.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            #set timestamp to discord time
            blocked_embed.timestamp = datetime.datetime.utcnow()
            await interaction.followup.send(embed=blocked_embed, ephemeral=True)
            await message.delete()

            try:
                #after timeout delete the message
                await message.delete(delay=30)
                return "blocked"
            except:
                #if it fails means it was hidden therefore we ignore
                pass
        
        return nsfw

    async def user_blacklist_actions(self, interaction, message, database):
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
            blacklisted_embed = disc.Embed(description=f"ㅤ\n**Your Account has been Locked**\n\nReason: {results[0][7]}\nㅤ",  color=0xff0000)
            #set blocked emoji as the thumbnail
            blacklisted_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1044880151017705512/1044883727689457664/padlock.png")
            
            await interaction.followup.send(embed=blacklisted_embed, ephemeral=True)
            await message.delete()

            try:
                #after timeout delete the message
                await message.delete(delay=30)
                #cancel original command
                return "user_blacklisted"
            except:
                #if it fails means it was hidden therefore we ignore
                pass
        
        return None

    async def target_blacklist_actions(self, interaction, user, message, database):
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query for all non nsfw quotes
        command = f"select * from users where uid={user.id}"
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
            print(f"\nWARNING: a user has attempted to access a blacklisted profile\nUser: {interaction.user.id}\nTarget: {user.id}\nReason: {results[0][7]}\nGuild: {interaction.guild.id}")
            #create blocked embed
            blacklisted_embed = disc.Embed(description=f"ㅤ\n\n**This QuoteBot Profile has been Locked\n**\nㅤ", color=0xff0000)
            #set blocked emoji as the thumbnail
            blacklisted_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1044880151017705512/1044883727689457664/padlock.png")

            await interaction.followup.send(embed=blacklisted_embed, ephemeral=True)
            await message.delete()

            try:
                #after timeout delete the message
                await message.delete(delay=30)
                #cancel original command
                return "target_blacklisted"
            except:
                #if it fails means it was hidden therefore we ignore
                pass
        
        return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(action_manager(bot), guilds = commands.Greedy[disc.Object])
