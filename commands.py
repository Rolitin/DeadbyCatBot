#----------------------------------------------------------------------------------#
from async_def import fetch_shrine_data, send_shrine_embeds
#----------------------------------------------------------------------------------#
async def fetch_shrine_info(ctx, bot):
    # Your existing function code using both ctx and bot
    data = await fetch_shrine_data()
    if data:
        await send_shrine_embeds(data, ctx.channel.id, bot)
    else:
        await ctx.send("Failed to fetch data from the API.")
#----------------------------------------------------------------------------------#
async def cmd_ping(ctx):
    await ctx.send("!pong")
#----------------------------------------------------------------------------------#