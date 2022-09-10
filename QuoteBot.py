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
        # main init
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default(), application_id=814379239930331157, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your quotes"))
        #dev init
        # super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default(), application_id=831626069789638656, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your quotes"))

    async def load_cogs(self):
        print("---\ Loading Quotebot")

        for cog in os.listdir(f'./cogs'): #loop through all folders in ./cogs

            print(f"   |---\ loading {cog}")

            for subdir, dirs, files in os.walk(f'./cogs/{cog}'): #get all folders in cog folder

                for filename in files: #loop through each file in folders

                    filepath = subdir + os.sep + filename #create filepath

                    if filepath.endswith('.py'): 

                        load_path = str(filepath).replace("/",".")[2:][:-3] #convert path to load path

                        await self.load_extension(f'{load_path}') #load the cog

                        console = load_path.split(".")
                        indent="   |    "

                        for item in console[2:]:
                            print(f'{indent}|---\ {item}.py')
                            indent+="|   "

                        print(f"{indent} |---> loaded {load_path}")

    

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

#main token
bot.run('ODE0Mzc5MjM5OTMwMzMxMTU3.G5Szyd.Bm7QwEI84R-PcLz0hRTkd1qQ8E4540N_HSvl_g')
#dev token
# bot.run('ODMxNjI2MDY5Nzg5NjM4NjU2.G3ZZO5.o55KqPwjt1z3NXt_xVjF0_Cgge7ZIJaA9qKssI')