import discord
from discord.errors import Forbidden
from discord.ext import commands 
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embedVar = discord.Embed(title="QuoteBot Help Menu", description="Store quotes quickly and easily", color=0x00ff00)
        embedVar.add_field(name="q!help", value="displays this message", inline=False)
        embedVar.add_field(name="q!invite", value="sends the invite link for Quotebot", inline=False)
        embedVar.add_field(name="q!info", value="displays info on QuoteBot", inline=False)
        embedVar.add_field(name="q!quote", value="usage: q!quote <@user/user#000> \nQuotes a random quote of a user\n",inline=False)
        embedVar.add_field(name="q!addquote", value="usage: q!addquote <@user/user#000> <quote> \nAdds a quote to their stored quotes\n\n",inline=False)
        embedVar.add_field(name="q!delquote", value="usage: q!delquote <@user/user#000> <part-of-quote> \nRemoves a quote from a users stored quotes\n\n",inline=False)
        embedVar.add_field(name="q!qowote", value="usage: q!qowote <@user/user#000> \nQuotes a random user but adds an uwu twist\n",inline=False)        
        embedVar.add_field(name="q!listquotes", value="usage: q!listquotes <@user>\n Prints all quotes stored for set user\n\n",inline=False)
        embedVar.add_field(name="q!inspire", value="usage: q!inspire\n Puts an inspirational quote into a #inspiration channel\n\n", inline=False)
        embedVar.add_field(name="q!setquotechannel", value="usage: q!setquotechannel (**Requires Manage Server**)\n Sets the current  channel as the quote channel\nCommands: **q!addquote** and **q!delquote** will be locked to this channel\n\n", inline=False)
        embedVar.add_field(name="q!setlogger", value="usage: q!setlogger (**Requires Manage Server)**\n Sets the current channel as the log channel\n\n Developed by vexi#0420", inline=False)
        try:
            await ctx.author.send(embed=embedVar)
            message = await ctx.send("Help has been sent!\n*check your dms*")
            await message.add_reaction("😇")
        except Forbidden:
            await ctx.send('Your dms are not open! use **q!qhelp** to get help sent in this channel or enable dms for server members')

    @commands.command()
    async def qhelp(self, ctx):
        embedVar = discord.Embed(title="QuoteBot Help Menu", description="Store quotes quickly and easily", color=0x00ff00)
        embedVar.add_field(name="q!help", value="displays this message", inline=False)
        embedVar.add_field(name="q!invite", value="sends the invite link for Quotebot", inline=False)
        embedVar.add_field(name="q!info", value="displays info on QuoteBot", inline=False)
        embedVar.add_field(name="q!quote", value="usage: q!quote <@user/user#000> \nQuotes a random quote of a user\n",inline=False)
        embedVar.add_field(name="q!addquote", value="usage: q!addquote <@user/user#000> <quote> \nAdds a quote to their stored quotes\n\n",inline=False)
        embedVar.add_field(name="q!delquote", value="usage: q!delquote <@user/user#000> <part-of-quote> \nRemoves a quote from a users stored quotes\n\n",inline=False)
        embedVar.add_field(name="q!qowote", value="usage: q!qowote <@user/user#000> \nQuotes a random user but adds an uwu twist\n",inline=False)        
        embedVar.add_field(name="q!listquotes", value="usage: q!listquotes <@user>\n Prints all quotes stored for set user\n\n",inline=False)
        embedVar.add_field(name="q!inspire", value="usage: q!inspire\n Puts an inspirational quote into a #inspiration channel\n\n", inline=False)
        embedVar.add_field(name="q!setquotechannel", value="usage: q!setquotechannel (**Requires Manage Server**)\n Sets the current  channel as the quote channel\nCommands: **q!addquote** and **q!delquote** will be locked to this channel\n\n", inline=False)
        embedVar.add_field(name="q!setlogger", value="usage: q!setlogger (**Requires Manage Server)**\n Sets the current channel as the log channel\n\n Developed by vexi#0420", inline=False)
        await ctx.send(embed=embedVar)


def setup(bot):
    bot.add_cog(Help(bot))
