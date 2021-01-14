import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import os
import pandas as pd
import logging
import logging.handlers
from datetime import datetime
import data
import transformer
import secrets
import logs

# Logging
logger = logging.getLogger("__main__")

load_dotenv()
token = os.getenv("TOKEN")

guildid = os.getenv("GUILDID")
guildid = int(guildid)

intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix=".", intents=intents)

transformer = transformer.transformer("CV_Tennis_Roster.xlsx")
data = data.data("CV_Tennis_Roster.csv")

blacklisttxt = open("blacklist.txt", "r")
blacklist = blacklisttxt.read().split(" ")
blacklisttxt.close()


@bot.event
async def on_ready():
    global lockout
    lockout = {}
    global token_list
    token_list = []
    list_guild_no_cmd = list(filter(lambda guild: 'cmd' not in [name.name for name in guild.text_channels], bot.guilds))
    if list_guild_no_cmd:
        for guild in list_guild_no_cmd:
            admin_role = get(guild.roles, name="Server Admin")
            overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
            }
            cmd_channel = await guild.create_text_channel('cmd', overwrites=overwrites)
            logger.info(f"'cmd' text channel created in f{str(guild)}")
            await cmd_channel.send('''This is where you will send commands to the Tennis Bot.

To recieve a token, please type in 'token' to recieve a special token''')
            await cmd_channel.send("")
        
    global guildobject
    guildlist = list(filter(lambda guildlist: guildlist.id == guildid, bot.guilds))
    guildobject = guildlist[0]
    
    logger.info("Bot is ready to go.")

@bot.event
async def on_member_join(member):
    logger.info(f"{member} has joined the server.")
    role = "Guest"
    try:
        await member.add_roles(discord.utils.get(member.guild.roles, name=role))
        logger.info(f"Assigned {member} the 'Guest' role.")
    except Exception as e:
        logger.error("Cannot assign role. Error: " + str(e))
    await member.send('''------------------------------------------------------------------------
For access to the CVHS Tennis Discord Server, please enter your **SCHOOL ID**

(ex: "123456")
------------------------------------------------------------------------
If you are an **Alumni**, please message **Coach Doil (Liod#4439)** for a token.
Copy and paste the token here for access into the server.''')
    
@bot.event
async def on_member_remove(member):
    logger.info(f"{member} has left the tennis server.")
    if data.discordidexists(str(member.id)):
        data.removeInServer(member.id)
        data.removediscordid(member.id)
        logger.info(f"Removed {member}'s discordid from the database'")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if str(message.channel.type) == "private":    
        blacklisttxt = open("blacklist.txt", "r")
        blacklist = blacklisttxt.read().split(" ")
        blacklisttxt.close()
        if str(message.author.id) in blacklist:
            logger.info(f"{str(message.author.id)} was blocked \
by blacklist.")
            await message.channel.send('''You've been locked \
out for too many failed attempts.
Please message Coach Doil (Liod#4439) to unlock.''')
            if message.author.id in lockout:
                del lockout[message.author.id]
        else:
            if message.author.id in lockout:
                if lockout[message.author.id] >= 15:
                    blacklisttxt = open("blacklist.txt", "a")
                    blacklisttxt.write(str(message.author.id) + " ")
                    blacklisttxt.close()
                    logger.info(f"Added user {str(message.author)} to blacklist.")
            else:
                lockout[message.author.id] = 0
                
            msg = message.content.strip()
            if len(msg) == 6:
                try:
                    msg = int(msg)
                    if bool(data.isInServer(msg)):
                        await message.channel.send("You are already in the server!")
                    else:
                        if data.auth(msg):
                            logger.info(f"{message.author} passed authentication.")
                            data.addDiscordId(msg, message.author.id)
                            data.addToServer(msg)
                            logger.info(f"Added {message.author}'s Discord information.")
                            stuarr = data.getStuArray(msg)
                            if stuarr[2] == "VB":
                                role = "Varsity Boys"
                            elif stuarr[2] == "VG":
                                role = "Varsity Girls"
                            elif stuarr[2] == "JVB":
                                role = "JV Boys"
                            elif stuarr[2] == "JVG":
                                role = "JV Girls"
                            try:
                                member = guildobject.get_member(message.author.id)
                                await member.add_roles(discord.utils.get(member.guild.roles, name=role))
                                await member.remove_roles(discord.utils.get(member.guild.roles, name="Guest"))
                                await message.channel.send(f"Congratulations {message.author.mention}, you're now in the CV Tennis Discord Server!")
                                logging.info(f"Gave {message.author} the {str(role)} role.")
                                tempnick = data.getFullName(msg)
                                await member.edit(nick=tempnick)
                                logging.info(f"Updated {message.author}'s nickname")
                            except Exception as e:
                                logger.error("Cannot assign role. Error: " + str(e))
                        else:
                            await message.channel.send("Student not found. Check for typos and commas and try again.")
                            lockout[message.author.id] += 1
                            logger.info(f"{message.author} failed authentication")
                except Exception as e:
                    logger.error("Error: " + str(e))
                    await message.channel.send("Student not found. Check for typos and commas and try again.")
                    lockout[message.author.id] += 1
            elif len(msg) == 8:
                if not data.discordidexists(message.author.id):
                    if message.content in token_list:
                        try:
                            logger.info(f"Valid token accepted from {message.author}")
                            for i in range(len(token_list)):
                                if token_list[i] == message.content:
                                    token_list.pop(i)
                            member = guildobject.get_member(message.author.id)
                            await member.add_roles(discord.utils.get(member.guild.roles, name="Alumni"))
                            await member.remove_roles(discord.utils.get(member.guild.roles, name="Guest"))
                            logger.info(f"Added {message.author} to the server and gave Alumni role")
                            await message.channel.send(f"Congratulations {message.author.mention}, you're now in the CV Tennis Discord Server!")
                        except Exception as e:
                            logger.error("Cannot assign role. Error: " + str(e))
                    else:
                        await message.channel.send("Token not found. Check for typos and try again.")
                        lockout[message.author.id] += 1
                        logger.error(f"Invalid token from {message.author}")
                else:
                    await message.channel.send("You are already in the server!")
                    
            else:
                await message.channel.send("Student not found. Check for typos and commas and try again.")
                lockout[message.author.id] += 1
                    
    else:        
        if message.channel.name == "cmd":
            try:
                if len(message.attachments) == 1:
                    if message.attachments[0].filename == "CV_Tennis_Roster.xlsx":
                        switch = False
                        try:
                            await message.attachments[0].save(message.attachments[0].filename)
                            transformer.setfile(message.attachments[0].filename)
                            transformer.updatecsv()
                            transformer.formatcsv()
                            data.setdata(transformer.getCsvName())
                            switch = True
                            await message.channel.send("Recieved New Roster!")
                            logger.info("Updated new roster!")        
                        except Exception as e:
                            logger.error("Could not update roster. Error: " + str(e))
                        try:
                            if switch:    
                                for member in guildobject.members:
                                    flip = True
                                    for i in member.roles:
                                        if i.name == "Alumni" or i.name == "Guest":
                                            pass
                                        else:
                                            try:
                                                await member.remove_roles(discord.utils.get(member.guild.roles, name=str(i)))
                                                await member.add_roles(discord.utils.get(guildobject.roles, name="Guest"))
                                                if flip:
                                                    await member.send('''------------------------------------------------------------------------
For access to the CVHS Tennis Discord Server, please enter your **SCHOOL ID**

(ex: "123456")
------------------------------------------------------------------------
If you are an **Alumni**, please message **Coach Doil (Liod#4439)** for a token.
Copy and paste the token here for access into the server.''')
                                                    flip = False
                                            except:
                                                pass
                                await message.channel.send("Sucessfully reset roles!")
                                logger.info("Reset all roles!")        
                            else:
                                logger.info("Could not reset roles beacuse a roster is not detected.")        
                        except Exception as e:
                            logger.error("Could not reset roles. Error: " + str(e))                    
                    else:
                        await message.channel.send('''Roster not detected. Attatchment \
invalid or attatchment's name is spelled incorrectly.
The correct spelling for the file is "CV_Tennis_Roster.xlsx"''')
                        logger.error("Roster not found.")
            except Exception as e:
                logger.error("Could not reset roster. Error: " + str(e))            
            await bot.process_commands(message)

@bot.command()
async def gettoken(ctx):
    if len(token_list) < 10:
        temp = secrets.token_hex(4)
        token_list.append(temp)
        
        embed = discord.Embed(
            colour = discord.Colour.red()
        )
        
        embed.add_field(name="New Token:", value=temp, inline=False)

        await ctx.send(embed=embed)
        logger.info(f"Generated new token: '{temp}'")
    else:
        await ctx.send('''Maximum number of tokens reached! (10)
Remove tokens from token list to generate more.''')

@bot.command()
async def listtokens(ctx):
    embed = discord.Embed(
        title = "Tokens",
        description = "-Tokens in Use",
        colour = discord.Colour.red()
    )
    count = 1
    for i in token_list:
        embed.add_field(name="#"+str(count)+")", value=str(i), inline=False)
        count += 1
    embed.set_footer(text=str(datetime.now().strftime("Date: %b %d, %Y  Time: %I:%M %p")))
    await ctx.send(embed=embed)
    logger.info("Got token list.")

@bot.command()
async def removetoken(ctx,*,number):
    try:
        number = int(number)
        removed = token_list[number-1]
        token_list.pop(number-1)
        await ctx.send(str(removed) + " removed from tokens!")
        logger.info(str(removed) + " removed from tokens!")
    except Exception as e:
        await ctx.send("Couldn't remove from tokens")
        logger.error("Couldn't remove from tokens. Error: " + str(e))

@bot.command()
async def getblacklist(ctx):
    embed = discord.Embed(
        title = "Blacklist",
        description = "-Users in the blacklist",
        colour = discord.Colour.blue()
    )
    
    blacklisttxt = open("blacklist.txt", "r")
    blacklist = blacklisttxt.read().split(" ")
    blacklisttxt.close()
    
    count = 1
    for i in blacklist:
        if i != "":
            embed.add_field(name="#"+str(count)+")", value="<@"+str(i)+">", inline=False)
        else:
            embed.add_field(name="#"+str(count)+")", value='None', inline=False)
        count += 1
    embed.set_footer(text=str(datetime.now().strftime("Date: %b %d, %Y  Time: %I:%M %p")))
    await ctx.send(embed=embed)
    logger.info("Got blacklist.")

@bot.command()
async def removeblacklist(ctx,*,number):
    try:
        number = int(number)
        blacklisttxt = open("blacklist.txt", "r")
        blacklist = blacklisttxt.read().split(" ")
        blacklisttxt.close()
        removed = blacklist[number-1]
        blacklist.pop(number-1)
        newlist = ""
        for i in blacklist:
            if i != "":
                newlist = newlist + str(i) + " "
        blacklisttxt2 = open("blacklist.txt", "w")
        blacklisttxt2.write(newlist)
        blacklisttxt2.close()
        if removed != "":
            await ctx.send("<@"+str(removed)+"> removed from blacklist!")
            logger.info(f"{removed} removed from blacklist!")
        else:
            await ctx.send("Please select a valid user.")
            logger.warning(f"Invalid user selected for blacklist removal.")
    except Exception as e:
        await ctx.send("Couldn't remove user from blacklist")
        logger.error("Couldn't remove user from blacklist. Error: " + str(e))

if __name__ == '__main__':
    logger_names = ['transformer','data','__main__']
    
    for logger_name in logger_names:
        logs.setUpLogger(logger_name)

bot.run(token)
logger.info('Bot has finished running and has ended all processes. \n')