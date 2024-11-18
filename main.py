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
    check_reminders.start()

@bot.hybrid_group(fallback="in")
async def remindme(ctx: commands.Context, time: str, message: str):
    time_pattern = re.compile(r'((?P<weeks>\d+)w)?((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?')
    match = time_pattern.fullmatch(time)
    if match:
        delta_kwargs = {key: int(value) for key, value in match.groupdict().items() if value is not None}
        reminder_time = (datetime.now() + timedelta(**delta_kwargs)).replace(second=0, microsecond=0)
        
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
        reminder = {
            'user': ctx.author.id,
            'time': reminder_time,
            'message': message
        }
        reminders.append(reminder)
        print(reminder)
        await ctx.send(f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M')}.")
    except:
        await ctx.send('Invalid time format. Please format the time like XX:MM.', ephemeral=True)

   
@tasks.loop(seconds=60)
async def check_reminders():
    now = datetime.now()
    to_remove = []
    for reminder in reminders:
        if reminder['time'] <= now:
            user = bot.get_user(reminder['user'])
            if user is None:
                user = await bot.fetch_user(reminder['user'])
            embed = discord.Embed(title="Reminder", description=reminder['message'], color=discord.Color.blue())
            embed.set_footer(text=f"Reminder for {user.name}")
            await user.send(embed=embed)
            to_remove.append(reminder)
    for reminder in to_remove:
        reminders.remove(reminder)
        
@check_reminders.before_loop
async def before_check_reminders():
    # Align the reminder checking loop to the start of the next minute
    now = datetime.now()
    seconds_past = now.second
    await asyncio.sleep(60 - seconds_past)
    print("Task aligned to the start of the next minute")
    

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)