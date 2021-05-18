import discord
from discord.ext import commands
import requests
import os
import json
import random

class Inspire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def logger(self, command, user, channel, color, guild,):
        channelsend = self.bot.get_channel(839963726941519873)
        sixteenIntegerHex = int(color.replace("#", ""), 16)
        readableHex = int(hex(sixteenIntegerHex), 0)
        time = datetime.datetime.now()  
        time = time.strftime(r"%x at %H:%M")
        logEmbed = discord.Embed(title=f"{user}", description=f"{command} \n\n <#{channel.id}> | guildID: {guild} | {time}", color=readableHex)
        logEmbed.set_thumbnail(url=user.avatar_url)
        await channelsend.send(embed=logEmbed)
        print(f"{user} | {command} | channelID: {channel.id} | guildID: {guild} | {time}")

    def get_inspire_quote(self):
        print("inspirequote is running")
        response = requests.get("https://zenquotes.io/api/random")
        print("got the response")
        json_data = json.loads(response.text)
        print("loading the json data")
        quote = json_data[0]['q']+"\n -"+json_data[0]['a']
        print("removed all extra parts.")
        return(quote)

    @commands.command()
    async def inspire(self, ctx):
        print("inspired,,,")
        for channel in ctx.guild.channels:
            if channel.name == "inspiration":
                print("Channel found")
                chid = channel.id
                print(chid)
                quote = self.get_inspire_quote()
                print("done")
                channel = self.bot.get_channel(chid)
                await channel.send(quote)
                await logger(command=f"Used **inspire** to send some inspiration", user=ctx.author, channel=ctx.channel, color="#42f5b3", guild=ctx.message.guild.id)

def setup(bot):
    bot.add_cog(Inspire(bot))