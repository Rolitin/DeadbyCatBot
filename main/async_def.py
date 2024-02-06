#----------------------------------------------------------------------------------#
#
# Asynchronous functions
#
#----------------------------------------------------------------------------------#
import requests
from datetime import datetime, timedelta
import pytz
import time
from config import usage_icons_urls
import discord
#----------------------------------------------------------------------------------#
async def fetch_shrine_data():
    response = requests.get('https://api.nightlight.gg/v1/shrine')
    if response.status_code == 200:
        return response.json()
    else:
        return None
#----------------------------------------------------------------------------------#
async def send_shrine_embeds(data, channel_id, bot):
    channel = bot.get_channel(channel_id)
    if channel:
        # Parse the start and end times
        starts_at = datetime.fromisoformat(data['data']['start']).replace(tzinfo=pytz.UTC)
        ends_at = datetime.fromisoformat(data['data']['end']).replace(tzinfo=pytz.UTC)
        now = datetime.now(pytz.UTC)
        
        remaining = ends_at - now
        if remaining.total_seconds() > 0:
            #
            days, remainder = divmod(remaining.total_seconds(), 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes = divmod(remainder, 60)[0]
            time_parts = []
            if days > 0:
                time_parts.append(f"{int(days)} days")
            if hours > 0:
                time_parts.append(f"{int(hours)} hours")
            if minutes > 0:
                time_parts.append(f"{int(minutes)} minutes")
            time_remaining_str = " ".join(time_parts)
        else:
            time_remaining_str = "Time's up!"

        shrine_info_embed = discord.Embed(
            title=f'**Week {data["data"]["week"]} Shrine Of Secrets**',
            description=f'**Starts**: <t:{int(starts_at.timestamp())}:F>\n'
                        f'**Ends**: <t:{int(ends_at.timestamp())}:F>\n'
                        f'**Time Remaining**: {time_remaining_str}',
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