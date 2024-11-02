import os
import random
import threading
import time
from typing import Final

import discord
from discord.ext import commands
from dotenv import load_dotenv

#==========Web server==========
from status_web import start_http_server

server_thread = threading.Thread(target=start_http_server, daemon=True)
server_thread.start()
#==========================

load_dotenv()
TOKEN: Final[str] = os.getenv('APP_TOKEN')

intents = discord.Intents()
intents.messages = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(intents=intents)

#==========Slash commands==========
@bot.slash_command(description="Roll a dice")
async def roll(ctx: discord.Interaction):
    response = "Look at that! It's `" + random.randint(1, 6) + "`"
    await ctx.response(response)

@bot.slash_command(description="Roll a dice")
async def roll_custom(ctx: discord.Interaction, dices):
    try:
        dices = int(dices)
    except ValueError:
        await ctx.response("Invalid number")
    if dices <= 1:
        await ctx.response("Invalid dice value")
    response = "Ooh! It's `" + random.randint(1, dices) + "`"
    await ctx.response(response)
#==================================


#==========Events==========
@bot.event
async def on_ready():
    time.sleep(0.5)
    print(f'"{bot.user.name}" is now ready!')

@bot.event
async def on_connect():
    try:
        await bot.sync_commands()
        print(f"{bot.user.name} connected.")
    except discord.HTTPException as e:
        print(f"Failed to sync commands: {e}")

#==========================

#=================================================================================================================================

def main():
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
