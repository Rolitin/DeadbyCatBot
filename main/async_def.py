#----------------------------------------------------------------------------------#
import requests
from datetime import datetime
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