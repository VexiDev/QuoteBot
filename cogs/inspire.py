import discord
from discord.ext import commands
import requests
import os
import datetime
import json
import random

class Inspire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            if "inspiration" in channel.name:
                print("Channel found")
                chid = channel.id
                print(chid)
                quote = self.get_inspire_quote()
                print("done")
                channel = self.bot.get_channel(chid)
                log = self.bot.get_cog("Logger")
                await channel.send(quote)
                await log.logger(command=f"Used **inspire** to send some inspiration", user=ctx.author, channel=ctx.channel, color="#42f5b3", guild=ctx.message.guild.id)

def setup(bot):
    bot.add_cog(Inspire(bot))