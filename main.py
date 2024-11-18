# This example requires the 'message_content' intent.

import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from datetime import datetime, timedelta
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

reminders = []

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f"Synced slash commands for {bot.user}")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f'Logged in as {bot.user}')

@bot.hybrid_group(fallback="in", scope=690239736547508238)
async def remindme(ctx: commands.Context, time: str, message: str):
    time_pattern = re.compile(r'((?P<weeks>\d+)w)?((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?')
    match = time_pattern.fullmatch(time)
    if match:
        delta_kwargs = {key: int(value) for key, value in match.groupdict().items() if value is not None}
        reminder_time =  datetime.now() + timedelta(**delta_kwargs)
        
        reminders.append({
            'user': ctx.author.id,
            'time': reminder_time,
            'message': message,
            'channel': ctx.channel.id
        })
        await ctx.send(f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')}.")
    else:
        await ctx.send('Invalid time format. Please use formats like 15m, 1h, 1h30m.')

@remindme.command()
async def at(ctx, time:str, message: str):
    try:
        reminder_time = datetime.strptime(time, '%H:%M').replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
        reminders.append({
            'user': ctx.author.id,
            'time': reminder_time,
            'message': message,
            'channel': ctx.channel.id
        })
        await ctx.send(f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')}.")
    except:
        await ctx.send('Invalid time format. Please format the time like XX:MM.', ephemeral=True)
  
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)