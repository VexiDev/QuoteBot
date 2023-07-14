import discord
import requests
import traceback as trace
from discord import app_commands
from discord.ext import commands

class content_filter(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def check_nsfw(self, quote, type="quote"):

        async def nsfwapi(quote):

            url = 'https://api.sightengine.com/1.0/text/check.json'

            data =  {
            'text':f'{quote}',
            'lang':'en',
            'list':'tli_aTs79afVyEDmo23PBJtBc',
            'mode':'standard',
            'api_user':f'1577683888',
            'api_secret':'KwUgHawuH53aRMPntbQA'
            }

            response = requests.post(url, data=data)

            response = response.json()

            return response
            

        async def blacklist_check(blacklist, i, type):
            try:
                if blacklist[i]['match'] == "rape" or blacklist[i]['match'] == "raped":
                    if type!="bio":
                        return True, False, False, f"Sexual Harassment ('{blacklist[i]['match']}')"
                    else:
                        return True, False, True, f"Sexual Harassment ('{blacklist[i]['match']}')"

                elif blacklist[i]['match'] == "retarded":
                    if type!="bio":
                        return True, False, False, f"Derogatory ('{blacklist[i]['match']}')"
                    else:
                        return True, False, True, f"Derogatory ('{blacklist[i]['match']}')"

                elif blacklist[i]['match'] == "nazi":
                    if type!="bio":
                        return True, False, False, f"Sensitive Topic ('{blacklist[i]['match']}')"
                    else:
                        return True, False, True, f"Sensitive Topic ('{blacklist[i]['match']}')"
                    
                else:
                    return None
            except:
                trace.print_exc()

        response = await nsfwapi(quote)

        profanity = response['profanity']['matches']
        blacklist = response['blacklist']['matches']
        personal = response['personal']['matches']
        link = response['link']['matches']

        # >> RETURN(NSFW, REVIEW, CANCEL, REASON) <<

        if len(personal) != 0:
            return False, True, True, f"Personal Information Detected ('{personal[0]['type']}')"
        
        if len(link) != 0:
            return False, False, True, "link"

        if len(profanity) != 0:
            for i in range(len(profanity)):
                if profanity[i]['type'] == 'discriminatory':
                    if type!="bio":
                        return True, True, False, f"Discrimination ('{profanity[i]['match']}')"
                    else:
                        return True, True, True, f"Discrimination ('{profanity[i]['match']}')"

                elif profanity[i]['type'] == 'derogatory':
                    if type!="bio":
                        return True, True, False, f"Derogatory ('{profanity[i]['match']}')"
                    else:
                        return True, True, True, f"Derogatory ('{profanity[i]['match']}')"

            if len(blacklist) != 0:
                for i in range(len(blacklist)):
                    blist_check = await blacklist_check(blacklist, i, type)
                    if blist_check != None:
                        return blist_check
                    else:
                        pass

            else:
                return False, False, False, "None"

        else:
            if len(blacklist) != 0:
                for i in range(len(blacklist)):
                    blist_check = await blacklist_check(blacklist, i, type)
                    if blist_check != None:
                        return blist_check
                    else:
                        pass


            else:
                return False, False, False, "None"

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(content_filter(bot), guilds = commands.Greedy[discord.Object])
