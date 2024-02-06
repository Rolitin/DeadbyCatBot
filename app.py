import discord
from discord.ext import commands
import requests
import json
from datetime import datetime
import pytz
import threading
import schedule
import time
import json
import config
import os

automated_message_channel_id = 1117895284773634128

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = config.token

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

usage_icons_urls = {
    'very low': 'https://i.imgur.com/J7HFy4H.png',
    'low': 'https://i.imgur.com/6u1Gu9P.png',
    'average': 'https://i.imgur.com/KvJVt0l.png',
    'high': 'https://i.imgur.com/wvpzkrq.png',
    'very high': 'https://i.imgur.com/wvBqMl8.png'
}

def send_automated_message():
    response = requests.get('https://api.nightlight.gg/v1/shrine')

    if response.status_code == 200:
        data = response.json()

        # First embed for the shrine information with dynamic timestamps
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

        channel = bot.get_channel(automated_message_channel_id)
        if channel:
            bot.loop.create_task(channel.send(embed=shrine_info_embed))
            # Individual embeds for each perk
            for perk in data['data']['perks']:
                usage_tier = perk["usage_tier"].lower()
                icon_url = usage_icons_urls.get(usage_tier, "")

                perk_embed = discord.Embed(
                    title=f'**{perk["name"]} ({perk["character"]})**',
                    description=f'**Usage Tier**: {perk["usage_tier"]}\n',
                    color=0x00ff00
                )
                perk_embed.set_thumbnail(url=icon_url)  # Set the icon image as thumbnail
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
                bot.loop.create_task(channel.send(embed=perk_embed))
        else:
            print("Channel not found.")
    else:
        print("Failed to fetch data from the API.")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("18:22").do(send_automated_message)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

@bot.command(name='shrine')
async def fetch_shrine_info(ctx):
    response = requests.get('https://api.nightlight.gg/v1/shrine')

    if response.status_code == 200:
        data = response.json()

        # First embed for the shrine information
        starts_at = datetime.fromisoformat(data['data']['start']).replace(tzinfo=pytz.UTC)
        ends_at = datetime.fromisoformat(data['data']['end']).replace(tzinfo=pytz.UTC)
        starts_at_unix = int(time.mktime(starts_at.timetuple()))
        ends_at_unix = int(time.mktime(ends_at.timetuple()))

        shrine_info_embed = discord.Embed(
            title=f'**Week {data["data"]["week"]} Shrine Of Secrets**',
            description=f'**Starts**: <t:{starts_at_unix}:F>\n'
                        f'**Ends**: <t:{ends_at_unix}:F>',
            color=0x0000ff
        )
        await ctx.send(embed=shrine_info_embed)
        
        # Individual embeds for each perk
        for perk in data['data']['perks']:
            usage_tier = perk["usage_tier"].lower()
            icon_url = usage_icons_urls.get(usage_tier, "")

            perk_embed = discord.Embed(
                title=f'**{perk["name"]} ({perk["character"]})**',
                description=f'**Usage Tier**: {perk["usage_tier"]}\n',
                color=0x00ff00
            )
            perk_embed.set_thumbnail(url=icon_url)  # Set the icon image as thumbnail
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
            await ctx.send(embed=perk_embed)
    else:
        await ctx.send("Failed to fetch data from the API.")

bot.run(TOKEN)
