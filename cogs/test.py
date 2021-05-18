import discord
from discord.ext import commands 
from . import logger

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("tested")

    @commands.command()
    async def logtest(self, ctx):
        print("started logging")
        self.logger(command='THIS IS A TEST LOG', user="logsender", channel="channelpog", color="#55ff21", guild="guildpog")
        print("done and logged")

def setup(bot):
    bot.add_cog(Test(bot))
