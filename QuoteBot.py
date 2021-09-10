import discord
from discord.ext.commands import CommandNotFound
from discord.ext import commands
import discord
import os

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True)
bot = commands.Bot(command_prefix='q!',intents=intents)
bot.remove_command('help')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Unkown command! Use **q!help** for a list of available commands")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"loaded {extension} c(p)og")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"unloaded {extension} c(p)og")

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"reloaded {extension} c(p)og")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename:
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

@bot.event
async def on_ready():
    print("Sucessfully connected to Quotebot!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="q!help"))

bot.run('ODE0Mzc5MjM5OTMwMzMxMTU3.YDc_xQ.Tud62bhKLaaWGGlpfWr-lJWZe5w')