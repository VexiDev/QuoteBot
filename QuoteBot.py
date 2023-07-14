import discord
import typing
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
import aiohttp
import asyncio
import traceback as trace
import topgg
import os

class QuoteBot(commands.Bot):

    def __init__(self) -> None:
        # Change 123 to your application id
        # main init
        # super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default(), application_id=814379239930331157, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your quotes"))
        #dev init
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default(), application_id=831626069789638656, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your quotes"))

    async def load_cogs(self):
        print("---\ Loading Quotebot")

        for cog in os.listdir(f'./cogs'): #loop through all folders in ./cogs

            print(f"   |---\ loading {cog}")

            for subdir, dirs, files in os.walk(f'./cogs/{cog}'): #get all folders in cog folder

                for filename in files: #loop through each file in folders

                    filepath = subdir + os.sep + filename #create filepath

                    if filepath.endswith('.py'): 
                        
                        load_path = str(filepath).replace("/",".").replace("\\",".")[2:][:-3] #convert path to load path
                        
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
        # ////// COMMENT OUT WHEN UPDATING STATS /////////
        await self.load_cogs()

        #sync commands
        # ////// COMMENT OUT WHEN UPDATING STATS /////////
        await bot.tree.sync()


    async def on_ready(self):
        #display complete message
        print(f"{self.user} has connected to Discord!")


#run bot
bot = QuoteBot()

@bot.command()
@commands.guild_only()
async def sync(ctx, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
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
async def update_stats(ctx):
    if ctx.author.id != 274213987514580993:
        return
    print('syncing server count with Bot lists...')
    try:
        #sync with topgg
        dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgxNDM3OTIzOTkzMDMzMTE1NyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjM3MTE2MTg5fQ.XHw1GJmlmspDotwYYWKBSpID2C4e0BTDIUvmb_Gmm4g"  # set this to your bot's Top.gg token
        bot.topggpy = topgg.DBLClient(bot, dbl_token)
        await bot.topggpy.post_guild_count()
        print(f"Posted TOPGG server count ({bot.topggpy.guild_count})")

        #sync with DiscordBots
        server_count = len(bot.guilds)
        print(server_count, type(server_count))

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": 'eyJhbGciOiJIUzI1NiJ9.eyJhcGkiOnRydWUsImlkIjoiMjc0MjEzOTg3NTE0NTgwOTkzIiwiaWF0IjoxNjc0MzAwMDg0fQ.BrmEDPAuSUN_ulHd0mN_X5cg9cvNfLpZ8zj_azGU9ZA', "Content-Type": 'application/json'}
            data = {"guildCount": server_count}

            async with await session.post(f"https://discord.bots.gg/api/v1/bots/814379239930331157/stats", headers=headers, json=data) as resp:

                print(await resp.text())


    except Exception as e:
        print(f"Failed to post server count\n{e.__class__.__name__}: {e}")

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
# bot.run('ODE0Mzc5MjM5OTMwMzMxMTU3.G5Szyd.Bm7QwEI84R-PcLz0hRTkd1qQ8E4540N_HSvl_g')
#dev token
bot.run('ODMxNjI2MDY5Nzg5NjM4NjU2.G3ZZO5.o55KqPwjt1z3NXt_xVjF0_Cgge7ZIJaA9qKssI')