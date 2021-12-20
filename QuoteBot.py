import discord
from discord.ext.commands import CommandNotFound
from discord.ext import commands
import discord
import asyncio
import os
from discord_components import *
# from discord_slash import SlashCommand 
import topgg

bot = commands.Bot(command_prefix='q!',intents=discord.Intents.all(),case_insensitive=True)
bot.remove_command('help')

# s_cmd = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename:
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        msg = await ctx.send("Unknown command! Use **q!help** for a list of available commands")
        await asyncio.sleep(5)
        await ctx.message.delete()
        await msg.delete()

@bot.command()
async def load(ctx, extension):
    if ctx.author.id != 274213987514580993:
        return
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"loaded {extension} c(p)og")

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id != 274213987514580993:
        return
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"unloaded {extension} c(p)og")

@bot.command()
async def reload(ctx, extension):
    if ctx.author.id != 274213987514580993:
        return
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"reloaded {extension} c(p)og")


@bot.event
async def on_ready():
    print(f"Sucessfully connected to {bot.user}!")
    misc = bot.get_cog("Misc")
    update = bot.get_cog("Updater")
    await update.v4_updater()
    dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgxNDM3OTIzOTkzMDMzMTE1NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjM3MTE2MTg5fQ.XHw1GJmlmspDotwYYWKBSpID2C4e0BTDIUvmb_Gmm4g"  # set this to your bot's Top.gg token
    bot.topggpy = topgg.DBLClient(bot, dbl_token)
    misc.update_stats.start()
    DiscordComponents(bot)
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="q!help"))

bot.run('ODE0Mzc5MjM5OTMwMzMxMTU3.YDc_xQ.Tud62bhKLaaWGGlpfWr-lJWZe5w')