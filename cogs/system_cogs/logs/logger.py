import discord
import datetime
import traceback
from discord import app_commands
from discord.ext import commands

class logger(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def logger(self, title, desc, user, color, guild, image=None):
        print(f"log|N:{title.replace('**','')}| GID:{guild}")
        sixteenIntegerHex = int(color.replace("#", ""), 16)
        readableHex = int(hex(sixteenIntegerHex), 0)
        # print("converted to readable hex")
        time = datetime.datetime.now()  
        time = time.strftime(r"%x at %H:%M")
        # print("Set time")
        logEmbed = discord.Embed(title=f"{title}",description=desc, color=readableHex)
        if image!=None:
            logEmbed.set_thumbnail(url=image)
        # print("Set embed")
        logEmbed.timestamp = datetime.datetime.utcnow()
        logEmbed.set_footer(text=f"QuoteBot | ID: {user.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
        try:
            logEmbed.set_author(name=user, url=discord.Embed.Empty, icon_url=user.display_avatar.url)
        except:
            pass
        # print("set embed author/passed invalid user")
        try:
            connect = self.bot.get_cog("database")
        except:
            traceback.print_exc()
        conn = connect.connectdb()
        c = conn.cursor()
        # print("connected and cursored")
        command = f"select * from channels where type = 'logger' and guild_id = {guild}"
        # print(command)
        c.execute(command)
        # print("executed")
        results = c.fetchall()
        # print(results)
        # print(results[0][2])
        conn.commit()
        c.close()
        conn.close()
        # print("closed connection")
        # print(len(results))
        if len(results) != 0:
            channelsend = self.bot.get_channel(results[0][2])
        else:
            print(f'no log channel for guild {guild}')
            return
        # print(channelsend)
        await channelsend.send(embed=logEmbed)
        print(channelsend.id)
        print("sent")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(logger(bot), guilds = [discord.Object(id=838814770537824378)])
