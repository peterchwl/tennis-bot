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
# import auth_handler

load_dotenv()
token = os.getenv("TOKEN")
guildid = os.getenv("GUILDID")

intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix=".", intents=intents)

transformer = transformer.transformer("Tennis Roster Excel.xlsx")
data = data.data("Tennis Roster CSV.csv")

lockout = {}

@bot.event
async def on_ready():
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
    guildobject = await bot.fetch_guild(guildid)
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
    await member.send('''For access to the CVHS Tennis Discord Server, please enter your **SCHOOL ID**, **LAST NAME**, **FIRST NAME**, and **ROLE**

For **ROLE**:
VB = Varsity Boys
VG = Varsity Girls
JVB = JV Boys
JVG = JV Girls

(ex: "123456 Lee Peter VB")
------------------------------------------------------------------------
***If you are an Alumni, please message Coach Doil (Liod#4439) for a token.
Copy and paste the token here for access into the server.***''')
    
@bot.event
async def on_member_remove(member):
    print(f"{member} has left a server.")
    # Make these commands later on in the future
    # if data.discord_id_exists(str(member.id)):
    #     data.remove_discord_id(member.id)

@bot.event
async def on_message(message):
    message_words = message.content.lower().strip().split(" ")
    print(message_words)
    if str(message.channel.type) == "private":
        pass
        #Check if user is already in the server
        #Check and update blacklist
        #Auth method
            #IN AUTH: inServer = True && add DiscordID
    if message.channel.name == "cmd":
        await bot.process_commands(message)

    
@bot.command()
async def updateroster(ctx, message):
    


    
bot.run(token)
        