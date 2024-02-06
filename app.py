import discord
from discord.ext import commands
import requests
import json
from datetime import datetime
import pytz
import threading
import schedule
import time
import config
import os
#----------------------------------------------------------------------------------#
# Channel ID for automated messages
automated_message_channel_id = 1117895284773634128
#----------------------------------------------------------------------------------#
# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True
#----------------------------------------------------------------------------------#
# Discord bot setup
bot = commands.Bot(command_prefix='!', intents=intents)
#----------------------------------------------------------------------------------#
# Discord bot token
TOKEN = config.token
#----------------------------------------------------------------------------------#
# Usage icons URLs
usage_icons_urls = {
    'very low': 'https://i.imgur.com/J7HFy4H.png',
    'low': 'https://i.imgur.com/6u1Gu9P.png',
    'average': 'https://i.imgur.com/KvJVt0l.png',
    'high': 'https://i.imgur.com/wvpzkrq.png',
    'very high': 'https://i.imgur.com/wvBqMl8.png'
}
#----------------------------------------------------------------------------------#
# Bot event for on_ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
#----------------------------------------------------------------------------------#
# Function to fetch and process shrine data
async def fetch_shrine_data():
    response = requests.get('https://api.nightlight.gg/v1/shrine')
    if response.status_code == 200:
        return response.json()
    else:
        return None
#----------------------------------------------------------------------------------#
# Function to create and send embeds
async def send_shrine_embeds(data, channel_id):
    channel = bot.get_channel(channel_id)
    if channel:
        starts_at = datetime.fromisoformat(data['data']['start']).replace(tzinfo=pytz.UTC)
        ends_at = datetime.fromisoformat(data['data']['end']).replace(tzinfo=pytz.UTC)
        starts_at_unix = int(time.mktime(starts_at.timetuple()))
        ends_at_unix = int(time.mktime(ends_at.timetuple()))

        shrine_info_embed = discord.Embed(
            title=f'**Week {data["data"]["week"]} Shrine Of Secrets**',
            description=f'**Starts**: <t:{starts_at_unix}:F>\n'
                        f'**Ends**: <t:{ends_at_unix}:F>',
            color=0xffa500
        )
        await channel.send(embed=shrine_info_embed)

        for perk in data['data']['perks']:
            usage_tier = perk["usage_tier"].lower()
            icon_url = usage_icons_urls.get(usage_tier, "")

            perk_embed = discord.Embed(
                title=f'**{perk["name"]} ({perk["character"]})**',
                description=f'**Usage Tier**: {perk["usage_tier"]}\n',
                color=0x00ff00
            )
            perk_embed.set_thumbnail(url=icon_url)
            perk_embed.add_field(
                name='**Bloodpoints**',
                value=f'{perk["bloodpoints"]}',
                inline=True
            )
            perk_embed.add_field(
                name='**Shards**',
                value=f'{perk["shards"]}',
                inline=True
            )
            await channel.send(embed=perk_embed)
    else:
        print("Channel not found.")
#----------------------------------------------------------------------------------#
# !shrine command
@bot.command(name='shrine')
async def fetch_shrine_info(ctx):
    data = await fetch_shrine_data()
    if data:
        await send_shrine_embeds(data, ctx.channel.id)
    else:
        await ctx.send("Failed to fetch data from the API.")
#----------------------------------------------------------------------------------#
# Function to send automated message
async def send_automated_message():
    data = await fetch_shrine_data()
    if data:
        await send_shrine_embeds(data, automated_message_channel_id)
    else:
        print("Failed to fetch data from the API.")
#----------------------------------------------------------------------------------#
# Scheduler setup
def run_scheduler():
    schedule.every().day.at("19:35").do(lambda: bot.loop.create_task(send_automated_message()))
    while True:
        schedule.run_pending()
        time.sleep(1)
#----------------------------------------------------------------------------------#
# Start scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()
#----------------------------------------------------------------------------------#
# Run the bot
bot.run(TOKEN)
#----------------------------------------------------------------------------------#