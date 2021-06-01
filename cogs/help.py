import discord
from discord.ext import commands 
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embedVar = discord.Embed(title="QuoteBot Help Menu", description="Displays all available commands for QuoteBot", color=0x00ff00)
        embedVar.add_field(name="q!help", value="displays this message", inline=False)
        embedVar.add_field(name="q!invite", value="sends the invite link for Quotebot")
        embedVar.add_field(name="q!info", value="displays info on QuoteBot")
        embedVar.add_field(name="q!setlogger", value="usage: q!setlogger\n Sets the current selected channel as the log channel")
        embedVar.add_field(name="q!setlogger", value="usage: q!setupdater\n Sets the current selected channel as the update channel")
        embedVar.add_field(name="q!quote", value="usage: q!quote <user> \nQuotes a random quote of a user\n",inline=False)
        embedVar.add_field(name="q!addquote", value="usage: q!addquote <user> <quote> \nAdds a quote to their stored quotes\n\n",inline=False)
        embedVar.add_field(name="q!delquote", value="usage: q!delquote <user> <part-of-quote> \nRemoves a quote from a users stored quotes\n\n",inline=False)
        embedVar.add_field(name="q!qowote", value="usage: q!qowote <user> \nQuotes a random user but adds an uwu twist\n",inline=False)        
        embedVar.add_field(name="q!listquotes", value="usage: q!listquotes <@user>\n Prints all quotes stored for set user\n\n",inline=False)
        embedVar.add_field(name="q!fight", value="usage: q!fight <@user1> <@user2> \n Initiate a showdown between two people\n\n",inline=False)
        embedVar.add_field(name="q!inspire", value="usage: q!inspire\n Puts an inspirational quote into #inspiration\n\n", inline=False)
        embedVar.add_field(name="q!permission", value="usage: q!permission <action> <user> <permission>\n**REQUIRES ADMINISTRATOR**\nActions = add/remove/show\npermissions = name of command (lowercase)\n\n",inline=False)        
        embedVar.add_field(name="q!geraltcock", value="usage: q!geraltcock\n**REQUIRES GERALTCOCK PERMISSION**\nSends geralt cock\n\n", inline=False)
        embedVar.add_field(name="q!dm", value="usage: q!dm <@user> <message>\n**REQUIRES DM PERMISSION**\nMakes the bot sends a custom dm to a user\n\n", inline=False)
        embedVar.add_field(name="q!dmspam", value="usage: q!dmspam <@user> <amount> <message>\n**REQUIRES DMSPAM PERMISSION**\n Makes the bot spam a custom dm to a user\n(sends 5msgs/5s)\n\n Developed by vexi#0420 and pastaslayer#8502", inline=False)
        message = await ctx.send("Help has been sent")
        await message.add_reaction("😇")
        await ctx.author.send(embed=embedVar)

def setup(bot):
    bot.add_cog(Help(bot))
