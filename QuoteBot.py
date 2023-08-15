import discord
import typing
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
import aiohttp
import asyncio
import traceback as trace
import topgg
import os

def read_env(file_path='.env'):
    env_vars = {}

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):  # Exclude comments and empty lines
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    return env_vars

env_vars = read_env()

class QuoteBot(commands.Bot):

    def __init__(self) -> None:
        # Change 123 to your application id
        # main init
        # super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default(), application_id=814379239930331157, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your quotes"))
        #dev init
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default(), application_id=831626069789638656, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="your quotes"))

    async def load_cogs(self):
        print("---\ Loading Quotebot")

        for cog in os.listdir(f'./cogs'):
            print(f"   |---\ loading {cog}")

            for subdir, dirs, files in os.walk(f'./cogs/{cog}'):

                for filename in files:

                    filepath = subdir + os.sep + filename

                    if filepath.endswith('.py'):
                        
                        load_path = str(filepath).replace("/",".").replace("\\",".")[2:][:-3]

                        if "database" in load_path:
                            from cogs.system_cogs.db.database import database
                            await bot.add_cog(database(bot, env_vars))
                        else:
                            await self.load_extension(f'{load_path}')

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
        dbl_token = f"{env_vars['Tgg_token']}"  # set this to your bot's Top.gg token
        bot.topggpy = topgg.DBLClient(bot, dbl_token)
        await bot.topggpy.post_guild_count()
        print(f"Posted TOPGG server count ({bot.topggpy.guild_count})")

        #sync with DiscordBots
        server_count = len(bot.guilds)
        print(server_count, type(server_count))

        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f'{env_vars["DBL_token"]}', "Content-Type": 'application/json'}
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
# bot.run(f"{env_vars['qb_prod_token']}")
#dev token
bot.run(f"{env_vars['qb_dev_token']}")