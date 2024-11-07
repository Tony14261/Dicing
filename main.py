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

random_responses = ["Look at that, it's [] !", " Ooh, it's []!", "Hmm.. Looks like you rolled []!", "Let's say.. []!", "Lemme see. It's []!", "Dicing.. []!", "Rolling, rolling, []!"]

@bot.slash_command(description="Roll a dice")
async def roll(ctx: discord.ApplicationContext):
    response = random_responses[random.randint(0, len(random_responses) - 1)].replace("[]", "`" + str(random.randint(1, 6)) + "`")
    await ctx.respond(response)

@bot.slash_command(description="Roll a custom dice")
async def roll_custom(ctx: discord.ApplicationContext, dices):
    try:
        dices = int(dices)
        if dices <= 1:
            await ctx.respond("Invalid dice value")
        else:
            response = random_responses[random.randint(0, len(random_responses) - 1)].replace("[]", "`" + str(random.randint(1, dices)) + "`")
            await ctx.respond(response)
    except ValueError:
        await ctx.respond("Invalid number")
#==================================


#==========Events==========
@bot.event
async def on_ready():
    time.sleep(0.5)
    print(f'"{bot.user.name}" is now ready!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching))
    await bot.change_presence(activity=discord.Activity(buttons=[{"label": "Open source", "url": "https://github.com/Tony14261/Dicing/"}, {"label": "Status", "url": "https://stats.uptimerobot.com/4CoTZy3oIe"}]))

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
