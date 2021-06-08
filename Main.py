from discord.ext.commands import CommandNotFound
from discord.ext import commands
from  builtins import any
from discord import Intents
import discord
import requests
import os
import asyncio
import random
import psycopg2
import threading

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
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print("Sucessfully connected to Quotebot!")
    statusType=0
    while True:
        if statusType == 0:
            await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="with q!help"))
            statusType = 1
        else:
            await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="for funny hahas"))
            statusType=0
        await asyncio.sleep(20)

bot.run('TOKEN')