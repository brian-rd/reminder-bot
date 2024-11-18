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
        
        reminder = {
            'user': ctx.author.id,
            'time': reminder_time,
            'message': message
        }
        reminders.append(reminder)
        
        await ctx.send(f"Reminder set for <t:{int(reminder_time.timestamp())}:f>.")
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
        await ctx.send(f"Reminder set for <t:{int(reminder_time.timestamp())}:f>.")
    except:
        await ctx.send('Invalid time format. Please format the time like XX:MM.')
        
class ReminderView(discord.ui.View):
    def __init__(self, reminder):
        super().__init__(timeout=None)
        self.reminder = reminder
        print(f'ReminderView initialized with reminder: {reminder}')

    @discord.ui.button(emoji="⏱️", label="10m", style=discord.ButtonStyle.secondary)
    async def snooze_10m(self, interaction: discord.Interaction, button: discord.ui.Button):
        reminder = self.reminder
        reminder['time'] = datetime.now() + timedelta(minutes=10)
        await interaction.response.send_message('Reminder snoozed for 10 minutes.')

    @discord.ui.button(emoji="⏱️", label="1h", style=discord.ButtonStyle.secondary)
    async def snooze_1h(self, interaction: discord.Interaction, button: discord.ui.Button):
        print('Snooze 1h button clicked')
        reminder = self.reminder
        reminder['time'] = datetime.now() + timedelta(hours=1)
        print(f'Reminder snoozed for 1 hour: {reminder}')
        await interaction.response.send_message('Reminder snoozed for 1 hour.')

    @discord.ui.button(emoji="🗑️", style=discord.ButtonStyle.danger)
    async def dismiss(self, interaction: discord.Interaction, button: discord.ui.Button):
        print('Dismiss button clicked')
        reminders.remove(self.reminder)
        print(f'Reminder dismissed: {self.reminder}')
        await interaction.response.send_message('Reminder dismissed.')
   
@tasks.loop(seconds=60)
async def check_reminders():
    now = datetime.now()
    for reminder in reminders:
        if reminder['time'] <= now:
            user = bot.get_user(reminder['user'])
            if user is None:
                user = await bot.fetch_user(reminder['user'])
            embed = discord.Embed(title="Reminder", description=reminder['message'], color=discord.Color.blue())
            embed.set_footer(text=f"Reminder for {user.name}")
            
            view = ReminderView(reminder)
            await user.send(embed=embed, view=view)


        
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