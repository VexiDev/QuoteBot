import discord
from discord.ext import commands
from  builtins import any
from discord import Intents
import requests
import os
import random
import asyncio
import traceback
import datetime
import math
import psycopg2

class Updater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def setupdater(self, ctx):
        if ctx.author.bot == True:
            return
        connect = self.bot.get_cog("Misc")
        # print('gotten connect')
        try:
            blist = await connect.checkblist(ctx, ctx.author)
        except:
            trace.print_exc()
        # print(f'connecting, {blist}')
        if blist is not None:
            if blist[1]=="global":
                # print('is global blist')
                await ctx.send(embed=blist[0])
                return
            else:
                pass
        else:
            pass
        print(f"Channel {ctx.channel.id} selected")
        channel = ctx.channel.id
        print(channel)
        guild = ctx.guild.id
        print(guild)
        misc = self.bot.get_cog('Misc')
        conn = misc.connectdb()
        c = conn.cursor()
        print("Connected and cursored")
        command = f"select id from channels where guild_id={guild} and type='update'"
        c.execute(command)
        print("executed")
        results = c.fetchall()
        results = str(results).replace(",)]", "")
        results = str(results).replace("[(", "")
        results = str(results).replace("[", "")
        results = str(results).replace("]", "")
        print(results)
        print(len(results))
        if len(results)==0:
            command5 = f"INSERT INTO channels(guild_id, channel_id, type) VALUES ({guild},{channel}, 'update')"
            print(command5)
            c.execute(command5)
            print("executed")
        else:
            command5 = f"UPDATE channels SET channel_id={channel} where id = {results};" 
            command6 = f"UPDATE channels SET type='update' where id = {results};"
            print(command5)
            print(command6)
            c.execute(command5)
            c.execute(command6)
        conn.commit()
        c.close()
        conn.close()
        message=f"Chat <#{ctx.channel.id}> has been set as the update channel"
        await ctx.send(message)
        print("Channel succesfully logged")
    
    @commands.command()
    async def testupdate(self, ctx, level="",*, updated=""):
        if ctx.author.bot == True:
            return
        print(ctx.author.id)
        if ctx.author.id == 274213987514580993:    
            await ctx.message.delete()
            if level=="major":
                connect = self.bot.get_cog("Misc")
                conn = connect.connectdb()
                c = conn.cursor()
                command = f"SELECT version FROM version WHERE id = 1"
                print(command)
                c.execute(command)
                results = c.fetchall()
                print(results)
                results = str(results).replace("[('(1,", "")
                results = str(results).replace(")',)]", "")
                print(results)
                conn.commit()
                c.close()
                conn.close()
                results = math.ceil(float(results))
                print(results)
                # conn = psycopg2.connect(
                # host="ec2-107-20-153-39.compute-1.amazonaws.com",
                # database="d54rrbkoagiuqg",
                # user="bcqrzmrdonxkml",
                # password="006986da51bca028a4af7404fde38e18c9f8a6208b495187b93d4744632b652d")
                # c = conn.cursor()
                # command = f"UPDATE version SET ver='{results}' WHERE id=1"
                # print(command)
                # c.execute(command)
                # conn.commit()
                # c.close()
                # conn.close()
                # print("executed")
                # #-------get updater channel---------
                # connect = self.bot.get_cog("Misc")
                # conn = connect.connectdb()
                # c = conn.cursor()
                # command2 = f"select * from channels where type = 'logger'"
                # print(command2)
                # c.execute(command2)
                # results2 = c.fetchall()
                # print(results2)
                # conn.commit()
                # c.close()
                # conn.close()
                #------------------------------------
                updateEmbed = discord.Embed(title=f"Updated to v{results}", description=f"{ctx.author.name} updated QuoteBot", color=0xf5e642)
                print("created embed")
                updateEmbed.add_field(name="Changelog:", value=f"{updated}",inline=False)
                print("added changelog")
                updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
                print("added image")
                print(f"length of results = {len(results2)}")
                await ctx.send(embed=updateEmbed)
                
            if level=="minor":
                connect = self.bot.get_cog("Misc")
                conn = connect.connectdb()
                c = conn.cursor()
                command = f"SELECT version FROM version WHERE id = 1"
                print(command)
                c.execute(command)
                results = c.fetchall()
                results = str(results).replace("[('(1,", "")
                results = str(results).replace(")',)]", "")
                print(results)
                conn.commit()
                c.close()
                conn.close()
                results = float(results)+0.1
                results = "{:.1f}".format(results)
                try:
                    print(f"Formated version value: {results}")
                    # conn = psycopg2.connect(
                    # host="ec2-107-20-153-39.compute-1.amazonaws.com",
                    # database="d54rrbkoagiuqg",
                    # user="bcqrzmrdonxkml",
                    # password="006986da51bca028a4af7404fde38e18c9f8a6208b495187b93d4744632b652d")
                    # c = conn.cursor()
                    # command = f'UPDATE version SET ver={results} WHERE id=1;'
                    # print(command)
                    # c.execute(command)
                    # conn.commit()
                    # c.close()
                    # conn.close()
                    #-------get updater channel---------
                    # connect = self.bot.get_cog("Misc")
                    # conn = connect.connectdb()
                    # c = conn.cursor()
                    # command2 = f"select * from channels where type = 'logger'"
                    # print(command2)
                    # c.execute(command2)
                    # results2 = c.fetchall()
                    # print(results2)
                    # conn.commit()
                    # c.close()
                    # conn.close()
                    #------------------------------------
                    updateEmbed = discord.Embed(title=f"Updated to v{results}", description=f"{ctx.author.name} updated QuoteBot", color=0xf5e642)
                    categories = updated.split("#")
                    for category in categories:
                        updateEmbed.add_field(name="Updated",value=f"{category}",inline=False)
                    updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
                    await ctx.send(embed=updateEmbed)
                except:
                    traceback.print_exc()
        else:
            await ctx.send("You are not authorised to use this command")



    @commands.command()
    async def update(self, ctx, level="",*, updated=""):
        if ctx.author.bot == True:
            return
        print(ctx.author.id)
        if ctx.author.id != 274213987514580993:    
            return
        await ctx.message.delete()
        if level=="major":
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            command = f"SELECT version FROM version WHERE id = 1"
            print(command)
            c.execute(command)
            results = c.fetchall()
            print(results)
            results = str(results).replace("[('(1,", "")
            results = str(results).replace(")',)]", "")
            print(results)
            conn.commit()
            c.close()
            conn.close()
            results = math.ceil(float(results))
            print(results)
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            command = f"UPDATE version SET ver='{results}' WHERE id=1"
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            conn.close()
            print("executed")
            #-------get updater channel---------
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            command2 = f"select * from channels where type = 'logger'"
            print(command2)
            c.execute(command2)
            results2 = c.fetchall()
            print(results2)
            conn.commit()
            c.close()
            conn.close()
            #------------------------------------
            updateEmbed = discord.Embed(title=f"Updated to v{results}", description=f"{ctx.author.name} updated QuoteBot", color=0xf5e642)
            print("created embed")
            updateEmbed.add_field(name="Changelog:", value=f"{updated}",inline=False)
            print("added changelog")
            updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
            print("added image")
            print(f"length of results = {len(results2)}")
            for total in range(len(results2)):
                sendchannel = self.bot.get_channel(results2[total][2])
                print(sendchannel)
                print(results2[total][2])
                await sendchannel.send(embed=updateEmbed)
            
        if level=="minor":
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            command = f"SELECT version FROM version WHERE id = 1"
            print(command)
            c.execute(command)
            results = c.fetchall()
            results = str(results).replace("[('(1,", "")
            results = str(results).replace(")',)]", "")
            print(results)
            conn.commit()
            c.close()
            conn.close()
            results = float(results)+0.1
            results = "{:.1f}".format(results)
            print(f"Formated version value: {results}")
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            command = f'UPDATE version SET ver={results} WHERE id=1;'
            print(command)
            c.execute(command)
            conn.commit()
            c.close()
            conn.close()
            #-------get updater channel---------
            connect = self.bot.get_cog("Misc")
            conn = connect.connectdb()
            c = conn.cursor()
            command2 = f"select * from channels where type = 'logger'"
            print(command2)
            c.execute(command2)
            results2 = c.fetchall()
            print(results2)
            conn.commit()
            c.close()
            conn.close()
            #------------------------------------
            updateEmbed = discord.Embed(title=f"Updated to v{results}", description=f"{ctx.author.name} updated QuoteBot", color=0xf5e642)
            updateEmbed.add_field(name="Changelog:", value=f"{updated}",inline=False)
            updateEmbed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/lightly-selected/30/loop-480.png")
            for total in range(len(results2)):
                sendchannel = self.bot.get_channel(results2[total][2])
                print(sendchannel)
                print(results2[total][2])
                await sendchannel.send(embed=updateEmbed)


    async def v4_updater(self):
        misc = self.bot.get_cog('Misc')
        conn = misc.connectdb()
        c = conn.cursor()
        command = f"SELECT * FROM version WHERE id = 1"
        print(command)
        c.execute(command)
        ver_results = c.fetchall()
        if ver_results[0][2]==True:
            print('already updated to v4')
            return
        elif ver_results[0][2]==False:
            print('Update available (v4) updating')
            command = f"UPDATE version SET ver=4.0 WHERE id=1"
            c.execute(command)
            update_msg = discord.Embed(title="NEW RELEASE!! QuoteBot 4.0", description="Now things are pretty", color=0x00ff00)
            update_msg.add_field(name='__New Command Names:__', value="**q!addquote <:member_join:908033530901192734> q!add\nq!delquote <:member_join:908033530901192734> q!delete\nq!listquotes <:member_join:908033530901192734> q!profile**\nCommands have been renamed for easier use and understanding, all commands are listed in **q!help**", inline=False)
            update_msg.add_field(name='__Profile System:__',value='All quotes are now stored in a users profile! Profiles have many features such as:\n**Bio:** Set a bio that syncs across all servers for your quotebot profile\n**Star Quotes:** Pin up to 3 Non-NSFW quotes to display on your profile across all servers!\n**Badges (Coming Soon):** Rewards for hitting certain achievements on quotebot (More info soon)', inline=False)
            update_msg.add_field(name='__NSFW System:__', value="There are still __no rules__ on what can and can't be added to QuoteBot BUT we will now be seperating quotes into two categories in an effort to have quotes be more neatly organized based on their content. Quotes detected to contain slurs or other such language will be auto-flagged as NSFW an sent in for review by our team. You can also send in a report with **q!request** if you wish for us to review a quote manually.\nYou can opt out of seeing NSFW quotes by running **q!togglensfw**\n\n***Reminder: IPs, Phone Numbers and other personals are not allowed on Quotebot***", inline=False)
            update_msg.add_field(name='__Request System:__', value="A way for you to communicate with me on any issues, user reports or suggestions you may have regarding Quotebot | **q!request <your-request>** | Abuse of this system will be met with a request blacklist", inline=False)
            update_msg.add_field(name='__Minor Update:__', value="- Database upgraded (faster)\n- All Quotebot response messages will now auto delete after a certain time\n- Logs have more info", inline=False)
            update_msg.add_field(name='__Future Updates:__', value="- Revamped Help system (sub categories, per command help)\n- File and Image linking\n- Quote Context", inline=False)
            update_msg.add_field(name='A huge thank you to all servers that are running quotebot!', value="[click here vote on top.gg](https://top.gg/bot/814379239930331157/vote)")
            update_msg.timestamp = datetime.datetime.utcnow()

            skiplist = [831369843353452584,711911329580974101,888091775347089479,911909706736484373,903122901039992893,908428900697272360,869428791041220618,760033559796121626,777189458860441610,869223276218560584,910116365870981140,692877530788528260,710974335006933014,761413354870800464,888397911665307668,844310426802978877,718119401878061138,881168352255541268,892871178182623263,879293540780343297,903917888572882954,836500033485930508,830218584424579102,903567189217538068,876961130495492146,826215830437363781,866083620539072512,900783388745662514,913109336694333502,802229707394252850,530284930119499776,904892027920076830,476157756190228521,882093368782491720,810318689584545863,817483064052547695,846454339551756318,921221588433661962]
            
            for guild in self.bot.guilds:
                if guild in skiplist:
                    print(f'skipping {guild.id} | {guild.name}')
                    pass
                else:
                    update_msg.set_footer(text=f"QuoteBot | ID: {guild.id}", icon_url="https://cdn.discordapp.com/attachments/844600910562066444/871953767115919400/quotebotpfp.png")
                    command = f"SELECT * FROM channels WHERE guild_id={guild.id}"
                    print(command)
                    c.execute(command)
                    results = c.fetchall()
                    update= None
                    log = None
                    quotes = None
                        
                    if len(results) != 0:
                        for channel in results:
                            if channel[3] == 'update':
                                update = channel[2]
                            elif channel[3] == 'logger':
                                log = channel[2]
                            elif channel[3] == 'quotes':
                                quotes = channel[2]

                        if update != None:
                            channel = self.bot.get_channel(update)
                        elif quotes != None:
                            channel = self.bot.get_channel(quotes)
                        elif log != None:
                            channel = self.bot.get_channel(log)
                        try:
                            await channel.send(embed=update_msg)
                        except:
                            pass
                    else:
                        for channel in guild.channels:
                            try:
                                await asyncio.sleep(0.5)

                                await channel.send(embed=update_msg)
                                break
                            except:
                                # traceback.print_exc()
                                pass
                

            command = f"UPDATE version SET v4updated=True WHERE id=1"
            c.execute(command)
            conn.commit()
            conn.close()
            print('Successfully updated to QuoteBot 4.0')

        else:
            print('unknown version return')
            return

def setup(bot):
    bot.add_cog(Updater(bot))