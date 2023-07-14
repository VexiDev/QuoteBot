import discord
import psycopg2
import datetime
from discord import app_commands
from discord.ext import commands

class server_lookup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def server_lookup(self, interaction: discord.Interaction, server: int, hidden=False):
        #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
        #Send loading message
        await interaction.response.send_message(embed=loading_embed, ephemeral=hidden)
        #assign message for future edits
        message = await interaction.original_response()

        #set database variable
        database = self.bot.get_cog("database")
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        
        #create query for total server quote count
        command = f"SELECT COUNT(*) FROM (SELECT DISTINCT quote FROM quotes where guild_id={server}) AS temp"
        #execute command
        c.execute(command)
        #get results of query
        total_quote_count=c.fetchall()

        #create query for total server normal quote count
        command = f"SELECT COUNT(*) FROM (SELECT DISTINCT quote FROM quotes where guild_id={server} and nsfw=False) AS temp"
        #execute command
        c.execute(command)
        #get results of query
        total_normal_count=c.fetchall()

        #create query for total server quote count
        command = f"SELECT COUNT(*) FROM (SELECT DISTINCT quote FROM quotes where guild_id={server} and nsfw=True) AS temp"
        #execute command
        c.execute(command)
        #get results of query
        total_nsfw_count=c.fetchall()

        #close database connection
        c.close()
        conn.close()

        #get guild object
        guild = await self.bot.fetch_guild(server)
        #make server info embed
        server_lookup_embed = discord.Embed(title=f"Server Lookup: {server}", description=f"-\nName: {guild.name}\nMembers: {guild.member_count}\n-")
        server_lookup_embed.add_field(name="Quote Info", value=f"Total count: {total_quote_count[0][0]}\nNormal count: {total_normal_count[0][0]}\nNSFW count: {total_nsfw_count[0][0]}")
        server_lookup_embed.set_thumbnail(url=guild.icon.url)
        server_lookup_embed.set_footer(text=f"QuoteBot | ID: {guild.id}", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        #set timestamp to discord time
        server_lookup_embed.timestamp = datetime.datetime.utcnow()

        view = self.PageNavigator()

        await message.edit(embed=server_lookup_embed, view=view)

        try:
            #after timeout delete the message
            await message.delete(delay=120)
            return
        except:
            #if it fails means it was hidden therefore we ignore
            pass

    class PageNavigator(discord.ui.View):
        def __init__(self, timeout=120):
            super().__init__(timeout=timeout)
            self.action = None

        #Create button to see server members
        @discord.ui.button(label='Members', style=discord.ButtonStyle.blurple, disabled=False)
        async def Back(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.action = 1
            self.stop()

        #Create button to see users NSFW quotes
        @discord.ui.button(label='Quotes', style=discord.ButtonStyle.green, disabled=False)
        async def Next(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.action = 2
            self.stop()

        #Create button to see users badges
        @discord.ui.button(label='NSFW', style=discord.ButtonStyle.red)
        async def Profile(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            self.action = 3
            self.stop()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(server_lookup(bot), guilds = commands.Greedy[discord.Object])
