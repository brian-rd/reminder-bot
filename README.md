# Discord Reminder Bot ⏰

A very simple, efficient Discord bot designed to help users set reminders in their DMs. This bot is built using `discord.py`.

## How to add
[Click here to add the bot to your server.](https://discord.com/oauth2/authorize?client_id=1308072545538277397)

## Motivation
I decided to build this because I wanted an easy way to get reminders across all my devices. I couldn't use iOS Reminders because I have a Windows PC and I'd prefer the reminders to be on both. Since I have Discord on both devices, I decided to build this Discord bot as it's far more convenient that using a dedicated third party application for reminders. Quickly building my own bot allows me to make it customisable and exactly how I want it.

## Features ✏️
- **Set Reminders**: Create reminders easily by specifying the time as either an exact time or a duration, and the reminder message. 
- **Receive Reminders in DMs**: All reminders are sent via Direct Messages to be more easily spotted. Embeds are used to improve appearance.
- **Snoozing Reminders**: Reminders can be snoozed with a single click, using the buttons sent with the reminder itself.

## Commands 📜
### `/remindme in <time> <message>`
Sets a reminder given a time period, given in the format WwDdHhMm (weeks, days, hours, minutes).
Examples:
- `/remindme in 2h Finish writing the Readme file`
- `/remindme in 2w2h Call grandma`

### `/remindme at <time> <message>`
Sets a reminder given an exact time, in the format HH:MM.
Examples:
- `/remindme at 13:00 Go to your lecture!`
- `/remindme at 18:42 Turn the oven off`

## Installation ⚙️
1. Clone this repository.
```git clone https://github.com/brian-rd/reminder-bot.git```
2. Navigate to the project directory.
```cd reminder-bot```
3. Install the dependencies.
```pip install -r requirements.txt```
4. Create a .env file in the project directory and add your Bot token.
```DISCORD_TOKEN=your_token_here```
5. Run the bot.
```python main.py```



