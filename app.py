#----------------------------------------------------------------------------------#
#
# Main Application
#
#----------------------------------------------------------------------------------#
import discord
from discord.ext import commands
#import requests
#import json
#from datetime import datetime
#import pytz
import threading
#import schedule
#import time
#import os
import config
from main.bot_event import bot_ready
from main.commands import fetch_shrine_info, cmd_ping
from main.async_def import send_shrine_embeds, fetch_shrine_data
from main.functions import run_scheduler
#----------------------------------------------------------------------------------#
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
#----------------------------------------------------------------------------------#
bot = commands.Bot(command_prefix='!', intents=intents)
#----------------------------------------------------------------------------------#
TOKEN = config.token
#----------------------------------------------------------------------------------#
@bot.event
async def on_ready():
    await bot_ready(bot)
#----------------------------------------------------------------------------------#
@bot.command(name='shrine')
async def shrine_command(ctx):
    await fetch_shrine_info(ctx, bot)
#----------------------------------------------------------------------------------#
@bot.command(name='ping')
async def ping_command(ctx):
    await cmd_ping(ctx)
#----------------------------------------------------------------------------------#
automated_message_channel_id = config.automated_message_channel_id
scheduler_thread = threading.Thread(target=run_scheduler, args=(bot, automated_message_channel_id))
scheduler_thread.start()
#----------------------------------------------------------------------------------#
bot.run(config.token)
#----------------------------------------------------------------------------------#