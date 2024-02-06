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
    'very low': 'https://drive.google.com/file/d/1qxbCOoU1nPMQ-1KbBevFdMvU16yJjglE/view?usp=drive_link',
    'low': 'https://drive.google.com/file/d/1AB-7QogvmqOuUCiuE07hA_I4A4gBnG3A/view?usp=drive_link',
    'high': 'https://drive.google.com/file/d/11QktT90rxNLphxHHmuQNZ3kYFjkPUdqj/view?usp=drive_link',
    'very high': 'https://drive.google.com/file/d/15B2qRJWPDGRiEMnLf9tQ2EDna8vAiHT7/view?usp=drive_link'
}

def send_automated_message():
    response = requests.get('https://api.nightlight.gg/v1/shrine')

    if response.status_code == 200:
        data = response.json()
        
        starts_at = datetime.fromisoformat(data['data']['start'])
        ends_at = datetime.fromisoformat(data['data']['end'])
        timezone = pytz.timezone('Europe/Berlin')
        starts_at_localized = starts_at.astimezone(timezone)
        ends_at_localized = ends_at.astimezone(timezone)
        starts_at_str = starts_at_localized.strftime("%B %d, %Y %I:%M %p %Z")
        ends_at_str = ends_at_localized.strftime("%B %d, %Y %I:%M %p %Z")

        current_time = datetime.now(timezone)
        time_remaining = ends_at_localized - current_time

        days_remaining = time_remaining.days
        hours_remaining, seconds_remaining = divmod(time_remaining.seconds, 3600)
        minutes_remaining = seconds_remaining // 60

        time_remaining_str = ""
        if days_remaining > 0:
            time_remaining_str += f'{days_remaining} days'
        if hours_remaining > 0:
            if time_remaining_str:
                time_remaining_str += ' '
            time_remaining_str += f'{hours_remaining} hours'
        if minutes_remaining > 0:
            if time_remaining_str:
                time_remaining_str += ' '
            time_remaining_str += f'{minutes_remaining} minutes'

        message = discord.Embed(
            title=f'**Week {data["data"]["week"]} Shrine Of Secrets**',
            description=f'**Starts**: {starts_at_str}\n'
                        f'**Ends**: {ends_at_str}\n'
                        f'**Time Remaining**: {time_remaining_str}',
            color=0xffa500
        )
        
        for perk in data['data']['perks']:
            message.add_field(
                name=f'**Name**: {perk["name"]}',
                value=f'**Character**: {perk["character"]}\n'
                      f'**ID**: {perk["id"]}\n'
                      f'**Usage**: {perk["usage_tier"]}',
                inline=False
            )

        channel = bot.get_channel(automated_message_channel_id)
        if channel:
            bot.loop.create_task(channel.send(embed=message))
        else:
            print("Channel not found.")
    else:
        print("Failed to fetch data from the API.")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("20:22").do(send_automated_message)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

@bot.command(name='shrine')
async def fetch_shrine_info(ctx, arg1=None, arg2=None, arg3=None):
    response = requests.get('https://api.nightlight.gg/v1/shrine')

    if response.status_code == 200:
        data = response.json()
        
        if arg1 == "perk" and arg2 is not None:
            perk_data = data['data']['perks'][int(arg2)]
            usage_tier = perk_data["usage_tier"].lower()
            svg_icon = usage_icons_urls.get(usage_tier, "")

            if arg3 == "usage":
                message = f'**Usage Tier**: {perk_data["usage_tier"]}\n{svg_icon}'
            elif arg3 == "id":
                message = f'**Perk ID**: {perk_data["id"]}'
            elif arg3 == "name":
                message = f'**Name**: {perk_data["name"]}'
            elif arg3 == "character":
                message = f'**Character**: {perk_data["character"]}'
            elif arg3 == "image":
                message = f'**Image URL**: {perk_data["image"]}'
            else:
                message = discord.Embed(
                    title=f'**{perk_data["name"]} ({perk_data["character"]})**',
                    description=f'**Usage**: {perk_data["usage_tier"]}\n{svg_icon}\n'
                                f'**Bloodpoints**: {perk_data["bloodpoints"]}\n'
                                f'**Shards**: {perk_data["shards"]}',
                    color=0x00ff00
                )
        else:
            starts_at = datetime.fromisoformat(data['data']['start']).replace(tzinfo=pytz.UTC)
            ends_at = datetime.fromisoformat(data['data']['end']).replace(tzinfo=pytz.UTC)
            starts_at_unix = int(time.mktime(starts_at.timetuple()))
            ends_at_unix = int(time.mktime(ends_at.timetuple()))

            message = discord.Embed(
                title=f'**Week {data["data"]["week"]} Shrine Of Secrets**',
                description=f'**Starts**: <t:{starts_at_unix}:F>\n'
                            f'**Ends**: <t:{ends_at_unix}:F>',
                color=0x0000ff
            )
            
            for perk in data['data']['perks']:
                usage_tier = perk["usage_tier"].lower()
                icon_url = usage_icons_urls.get(usage_tier, "")

                message.add_field(
                    name=f'**{perk["name"]}**',
                    value=f'**Character**: {perk["character"]}\n'
                        f'**Usage**: ![Usage Tier]({icon_url})',  # This is Markdown for embedding images
                    inline=False
                )

        await ctx.send(embed=message)
    else:
        await ctx.send("Failed to fetch data from the API.")

bot.run(TOKEN)
