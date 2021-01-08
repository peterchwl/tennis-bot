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
# import gettoken as tk
import secrets

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
            await cmd_channel.send('''This is where you will send commands to the Tennis Bot.

To recieve a token, please type in 'token' to recieve a special token''')
            await cmd_channel.send("")
        
    global guildobject
    guildlist = list(filter(lambda guildlist: guildlist.id == guildid, bot.guilds))
    guildobject = guildlist[0]
    print("Bot is ready.")
    #Log: Bot is ready

@bot.event
async def on_member_join(member):
    print(f"{member} has joined a server.")
    role = "Guest"
    try:
        await member.add_roles(discord.utils.get(member.guild.roles, name=role))
        #Log: Gave member role
    except Exception as e:
        await ctx.send("Cannot assign role. Error: " + str(e))
        #Log: Cannot assign role
    await member.send('''For access to the CVHS Tennis Discord Server, please enter your **SCHOOL ID**, **FIRST NAME**, **LAST NAME**, and **ROLE**

For **ROLE**:
VB = Varsity Boys
VG = Varsity Girls
JVB = JV Boys
JVG = JV Girls

(ex: "123456, Peter, Lee, VB")
------------------------------------------------------------------------
***If you are an Alumni, please message Coach Doil (Liod#4439) for a token.
Copy and paste the token here for access into the server.***''')
    
@bot.event
async def on_member_remove(member):
    print(f"{member} has left a server.")
    if data.discordidexists(str(member.id)):
        data.removeInServer(member.id)
        data.removediscordid(member.id)

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
            await message.channel.send('''You've been locked out for too many failed attempts.
Please message Coach Doil (Liod#4439) to unlock.''')
            if message.author.id in lockout:
                del lockout[message.author.id]
        else:
            if message.author.id in lockout:
                if lockout[message.author.id] >= 5:
                    blacklisttxt = open("blacklist.txt", "a")
                    blacklisttxt.write(str(message.author.id) + " ")
                    blacklisttxt.close()
            else:
                lockout[message.author.id] = 0
            message_words = message.content.lower().split(",")
            for i in range(len(message_words)):
                message_words[i] = message_words[i].strip()
            if len(message_words) == 4:
                try:
                    message_words[1], message_words[2] = message_words[2], message_words[1]
                    message_words[1] = message_words[1].capitalize()
                    message_words[2] = message_words[2].capitalize()
                    message_words[3] = message_words[3].upper()
                    message_words[0] = int(message_words[0])
                    if bool(data.isInServer(message_words[0])):
                        await message.channel.send("You are already in the server!")
                    else:
                        if data.auth(message_words):
                            data.adddiscordid(message_words[0], message.author.id)
                            data.addToServer(message_words[0])
                            if message_words[3] == "VB":
                                role = "Varsity Boys"
                            elif message_words[3] == "VG":
                                role = "Varsity Girls"
                            elif message_words[3] == "JVB":
                                role = "JV Boys"
                            elif message_words[3] == "JVG":
                                role = "JV Girls"
                            try:
                                member = guildobject.get_member(message.author.id)
                                await member.add_roles(discord.utils.get(member.guild.roles, name=role))
                                await member.remove_roles(discord.utils.get(member.guild.roles, name="Guest"))
                                await message.channel.send(f"Congratulations {message.author.mention}, you're now in the CV Tennis Discord Server!")
                                tempnick = message_words[2] + " " + message_words[1]
                                await member.edit(nick=tempnick)
                            except Exception as e:
                                print("Cannot assign role. Error: " + str(e))    
                        else:
                            await message.channel.send("Student not found. Check for typos and commas and try again.")
                            lockout[message.author.id] += 1
                except Exception as e:
                    print("Error: " + str(e))
                    await message.channel.send("Student not found. Check for typos and commas and try again.")
                    lockout[message.author.id] += 1
            elif len(message_words) == 1:
                if message.content in token_list:
                    try:
                        for i in range(len(token_list)):
                            if token_list[i] == message.content:
                                token_list.pop(i)
                        member = guildobject.get_member(message.author.id)
                        await member.add_roles(discord.utils.get(member.guild.roles, name="Alumni"))
                        await member.remove_roles(discord.utils.get(member.guild.roles, name="Guest"))
                        await message.channel.send(f"Congratulations {message.author.mention}, you're now in the CV Tennis Discord Server!")
                    except Exception as e:
                        print("Cannot assign role. Error: " + str(e))
                else:
                    await message.channel.send("Token not found. Check for typos and try again.")
                    lockout[message.author.id] += 1
                
            else:
                await message.channel.send("Student not found. Check for typos and commas and try again.")
                lockout[message.author.id] += 1 
                    
    else:        
        if message.channel.name == "cmd":
            if len(message.attachments) == 1 and message.attachments[0].filename == "CV_Tennis_Roster.xlsx":
                await message.attachments[0].save(message.attachments[0].filename)
                transformer.setfile(message.attachments[0].filename)
                transformer.updatecsv()
                transformer.formatcsv()
                data.setdata(transformer.getCsvName())
            await bot.process_commands(message)

@bot.command()
async def gettoken(ctx):
    temp = secrets.token_hex(4)
    token_list.append(temp)
    await ctx.send(temp)
    
@bot.command()
async def resetallroles(ctx):
    for member in ctx.guild.members:
        flip = True
        for i in member.roles:
            if i.name == "Alumni":
                pass
            else:
                try:
                    await member.remove_roles(discord.utils.get(member.guild.roles, name=str(i)))
                    await member.add_roles(discord.utils.get(ctx.guild.roles, name='Guest'))
                    if flip:
                        await member.send('''For access to the CVHS Tennis Discord Server, please enter your **SCHOOL ID**, **FIRST NAME**, **LAST NAME**, and **ROLE**

For **ROLE**:
VB = Varsity Boys
VG = Varsity Girls
JVB = JV Boys
JVG = JV Girls

(ex: "123456, Peter, Lee, VB")
------------------------------------------------------------------------
***If you are an Alumni, please message Coach Doil (Liod#4439) for a token.
Copy and paste the token here for access into the server.***''')
                        flip = False
                except:
                    pass

@bot.command()
async def getblacklist(ctx):
    embed = discord.Embed(
        title = "Blacklist",
        description = "--Users in the blacklist",
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
        await ctx.send("<@"+str(removed)+"> removed from blacklist!")
    except:
        pass

bot.run(token)