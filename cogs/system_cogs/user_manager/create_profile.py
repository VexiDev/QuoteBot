import discord
import datetime
from discord import app_commands
from discord.ext import commands

class profile_creator(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def creator(self, user):
        #define database variable
        database = self.bot.get_cog("database")
        #connect to database
        conn = database.connect()
        #open cursor
        c = conn.cursor()
        #create query
        command = f"select * from users where uid={user.id}" 
        #execute command
        c.execute(command)
        #get results
        result = c.fetchall()
        #if no profile found create one
        if len(result) == 0:
            #get current time
            date = datetime.datetime.now()
            #create profile creation query
            command = f"insert into users(uid, nsfw, global_blist, support_blist,support_cooldown, support_time, blist_reason, bio) values({user.id}, True, False, False, False, '{date}', 'None', 'None')"
            #execute commnad
            c.execute(command)
            #commit profile creation
            conn.commit()

        #close connection
        c.close()

async def setup(bot: commands.Bot) -> None:
        await bot.add_cog(profile_creator(bot), guilds = commands.Greedy[discord.Object])
