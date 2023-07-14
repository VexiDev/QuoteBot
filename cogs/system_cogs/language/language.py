import discord
from discord import app_commands
from discord.ext import commands
import os
import json

class language(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def get_server_language(self, guild_id):
        #check db for server language setting then iterate through ../messages/{language}//{message_file}.json and load the json as a dict
        #set database variable
        database = self.bot.get_cog("database")

        #get server language setting
        #connect to database
        conn = database.connect()
        #set database cursor
        c = conn.cursor()
        #create query to get user informtion
        command = f"select language from guilds where guild_id={guild_id}"
        #execute command
        c.execute(command)
        #get results of query
        server_settings=c.fetchall()
        #close database connection
        c.close()
        conn.close()

        #check if the server has a language setting
        if server_settings == None:
            #if no language setting set to default
            server_settings = "en"
        else:
            #if language setting exists set to that
            server_settings = server_settings[0][0]

        #return the server language setting
        return server_settings

    async def select_language(self, language, message_file):
        #iterate through ../messages/{language}/{message_file} and load the json as a dict

        # Get the root directory of the project
        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Remove everything after the /quote-bot-420/ from the path
        relative_path = str(root_dir).split("\quote-bot-420\\")[0]

        # Construct the path to the language file
        path = os.path.join((relative_path+"\quote-bot-420\\"), f"messages\{language}\{message_file}")
        print(f"loaded language path: ", path)

        # Open the language file using the desired path
        with open(path, "r") as f:
            # Load the JSON as a dict
            language_file = json.load(f)

        #return the language file
        return language_file


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(language(bot), guilds = [discord.Object(id=838814770537824378)])
