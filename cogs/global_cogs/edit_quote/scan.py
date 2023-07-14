import discord
import psycopg2
import humanize
import asyncio
import openai
import time
import aiohttp
import json
import traceback
from datetime import datetime
from discord import app_commands
from discord.ext import commands

class scan(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def quote_scan(self, interaction, channel, destination):
         #--------LOADING MENU---------
        #Create loading embed for profile
        loading_embed = discord.Embed(description="<a:loading:892534287415525386> **Processing Request**", color=0x068acc)
        #Send loading message
        await interaction.response.send_message(embed=loading_embed, ephemeral=True)
        #assign message for future edits
        origin_message = await interaction.original_response()
        
        #set database variable
        database = self.bot.get_cog("database")
        
        #------Pass System Checks-----
        #check maintenance
        #check if user is a bot
        if interaction.user.bot:
            #if is a bot cancel request
            is_bot_embed = discord.Embed(title="Bots cannot use QuoteBot", color=0xe02f2f)
            await origin_message.edit(embed=is_bot_embed)
            try:
                #after timeout delete the message
                await origin_message.delete(delay=5)
                return
            except:
                #if it fails means it was hidden therefore we ignore
                pass

        await self.scan_channel(interaction, origin_message, channel, destination)



    async def scan_channel(self, interaction, origin_message, channel, destination):
        
        scan_ongoing_embed = discord.Embed(title="Scanning Channel...", description="This may take a while depending on the size of the channel", color=0x068acc)
        scan_ongoing_embed.set_footer(text=f"QuoteBot | ID: TESTING /SCAN", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        await origin_message.edit(embed=scan_ongoing_embed)
        
        quotes_found = []

        quotes = [message async for message in channel.history(limit=None, oldest_first=True)]

        async def process_message(message):
            if not message.author.bot:
                result = await self.gpt_identify(message.content)
                print(result)
                await asyncio.sleep(1)
                try:
                    result = json.loads(result)
                    if result['isQuote'] == True:
                        print("\n-Quote Found-")
                        filter_result = await self.gpt_filter(result['quote'])
                        print(filter_result)
                        filter_json = json.loads(filter_result)
                        quotes_found.append([result['quote'], filter_json])
                        print("-Filter applied-\n")
                    else:
                        print("\n-Not a Quote-\n")
                except:
                    pass

        # Process messages one by one
        for message in quotes:
            await process_message(message)

        scan_complete_embed = discord.Embed(title="Scan Complete", description=f"**Quotes Found:** {len(quotes_found)}\n**Sending quotes to <#{destination.id}>", color=0x068acc)
        scan_complete_embed.set_footer(text=f"QuoteBot | ID: TESTING /SCAN", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        await origin_message.edit(embed=scan_complete_embed)

        await self.convert_to_quote(interaction, quotes_found, destination)


    async def convert_to_quote(self, interaction, quotes_found, destination):

        for quote in quotes_found:
            if len(quote[1]['detections']) == 0:
                filter = 'None'
            else:
                filter = quote[1]['detections']

            quote_embed = discord.Embed(title=f"{quote[0]}", description=f"**Filter Results:** {filter}", color=0x068acc)
            quote_embed.set_footer(text=f"QuoteBot | ID: TESTING /SCAN", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
            
            await destination.send(embed=quote_embed)
            await asyncio.sleep(1)

        scan_process_complete_embed = discord.Embed(title="Scan Process Complete", description=f"**Quotes Sent:** {len(quotes_found)}\n**Channel:** <#{destination.id}>", color=0x068acc)
        scan_process_complete_embed.set_footer(text=f"QuoteBot | ID: TESTING /SCAN", icon_url="https://cdn.discordapp.com/attachments/916091272186454076/1017973024680579103/quote_botttt.png")
        await interaction.followup.send(embed=scan_process_complete_embed, ephemeral=True)
        

    async def gpt_identify(self, message):
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
        }
        url = 'https://api.openai.com/v1/chat/completions'
        
        # Prepare the payload
        prompt = f"Determine if the following represents a quote considering its structure, quotation marks and author name: {message}"
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "As a multilingual AI, determine if the message is a representation of a quote. Return JSON with 'isQuote' (boolean) and 'quote' (message or null)."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100, 
            "n": 1
        }

        # Send the request and get the response
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(payload), headers=headers) as resp:
                response = await resp.json()

        # Error handling
        if 'choices' not in response:
            print("API error:", response)
            return None
        
        result = response['choices'][0]['message']['content']

        return result

    async def gpt_filter(self, message):
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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'
        }
        url = 'https://api.openai.com/v1/chat/completions'

        # Prepare the payload
        prompt = f"In the language of the message scan for: light innuendos ('light_sexual_content'), explicit sexual content ('aggressive_sexual_content'), derogatory language ('derogatory'), light ('l_profanity') and heavy profanity ('h_profanity'), personal info ('personals'), sensitive topics ('sensitive'). Each detection must include: 'type' (category key), 'content' (list of detected message parts). If no detections, 'detections' should be an empty list. \nMessage: {message}"
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "As a multilingual AI moderation system, analyze text. Respond in JSON with 'language': '<language-abbreviation>', 'scanned_message', and 'detections'. Detection settings are user-provided. Always use JSON."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "n": 1
        }

        # Send the request and get the response
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(payload), headers=headers) as resp:
                response = await resp.json()
        
        # Error handling
        if 'choices' not in response:
            print("API error:", response)
            return None
        
        result = response['choices'][0]['message']['content']

        return result

    # async def scan_message(self, interaction,origin_message, message):
        
    #     #check if message is a quote using chat gpt
    #     result = await self.gpt_identify(message)
    #     print(result)
    #     result = json.loads(result)

    #     if result['isQuote'] == True:
    #         print('Quote identified, running filter...')

    #         filter_result = await self.gpt_filter(result['quote'])

    #         print("\nfiltered: ", filter_result)

    #         await interaction.followup.send(filter_result)

    #     else:
    #         print('not a quote, ignoring...')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(scan(bot), guilds = commands.Greedy[discord.Object])
