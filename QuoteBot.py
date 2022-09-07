import discord
import typing
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import aiohttp
import asyncio
import traceback as trace
import os



class QuoteBot(commands.Bot):

    def __init__(self) -> None:
        # Change 123 to your application id
        super().__init__(command_prefix="q!", intents=discord.Intents.all(), application_id=831626069789638656, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your quotes"))

    async def load_cogs(self):
        print("---\ Loading Quotebot")

        for cog in os.listdir(f'./cogs'): #loop through all folders in ./cogs

            print(f"   |---\ loading {cog}")

            for subdir, dirs, files in os.walk(f'./cogs/{cog}'): #get all folders in cog folder

                for filename in files: #loop through each file in folders

                    filepath = subdir + os.sep + filename #create filepath

                    if filepath.endswith('.py'): 

                        extpath = str(filepath).replace("/",".")[2:][:-3] #convert path to load path

                        await self.load_extension(f'{extpath}') #load the cog

                        console = extpath.split(".")
                        indent="   |    "

                        for item in console[2:]:
                            print(f'{indent}|---\ {item}.py')
                            indent+="|   "

                        print(f"{indent} |---> loaded {extpath}")

    

    async def setup_hook(self) -> None:
        #set session to prevent close error
        self.session = aiohttp.ClientSession() 

        #run cog load function
        await self.load_cogs()

        #sync commands with dev server (!!! create auto syncer !!!)
        await bot.tree.sync()


    async def on_ready(self):
        #display complete message
        print(f"{self.user} has connected to Discord!")


#run bot
bot = QuoteBot()

@bot.command()
@commands.guild_only()
async def sync(
  ctx, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.command()
async def load(ctx, extension):
    if ctx.author.id != 274213987514580993:
        return
    try:
        await bot.load_extension(f'{extension}')
        await ctx.send(f"loaded {extension}")
    except:
        trace.print_exc()

@bot.command()
async def unload(ctx, extension):
    if ctx.author.id != 274213987514580993:
        return
    try:        
        await bot.unload_extension(f'{extension}')
        await ctx.send(f"unloaded {extension}")
    except:
        trace.print_exc()
        
@bot.command()
async def reload(ctx, extension):
    if ctx.author.id != 274213987514580993:
        return
    try:
        await bot.unload_extension(f'{extension}')
        await bot.load_extension(f'{extension}')
        await ctx.send(f"reloaded {extension}")
    except:
        trace.print_exc()
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        msg = await ctx.send("Unknown command! Use **q!help** for a list of available commands")
        await asyncio.sleep(5)
        await ctx.message.delete()
        await msg.delete()

bot.run('ODE0Mzc5MjM5OTMwMzMxMTU3.G5Szyd.Bm7QwEI84R-PcLz0hRTkd1qQ8E4540N_HSvl_g')
