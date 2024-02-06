#----------------------------------------------------------------------------------#
#import threading
import schedule
import time
from config import scheduled_time
from .async_def import fetch_shrine_data, send_shrine_embeds
#----------------------------------------------------------------------------------#
async def send_automated_message(bot, channel_id):
    data = await fetch_shrine_data()
    if data:
        await send_shrine_embeds(data, channel_id, bot)
    else:
        print("Failed to fetch data from the API.")
#----------------------------------------------------------------------------------#
def run_scheduler(bot, channel_id):
    schedule.every().day.at(scheduled_time).do(lambda: bot.loop.create_task(send_automated_message(bot, channel_id)))
    while True:
        schedule.run_pending()
        time.sleep(1)
#----------------------------------------------------------------------------------#