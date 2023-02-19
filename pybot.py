import discord
from discord.ext import commands
import random

from ipwhois import IPWhois
import json
import datetime

import config

def get_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime = secondsToText(uptime_seconds)

    return uptime

def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{} days, ".format(int(days)) if days else "") + \
    ("{} hours, ".format(int(hours)) if hours else "") + \
    ("{} minutes, ".format(int(minutes)) if minutes else "") + \
    ("{} seconds, ".format(int(seconds)) if seconds else "")
    return result

def get_christmas(date):
    """Returns the date of the Christmas of the year of the date"""
    next_xmas = datetime.datetime(date.year, 12, 25)
    if next_xmas < date:
        next_xmas = datetime.datetime(date.year+1, 12, 25)
    return next_xmas

def days_to_xmas(input_date):
    ans = (get_christmas(input_date) - input_date).days
    return ans

description = 'pybot'
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def subtract(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left - right)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def ipwhois(ctx, ip: str):
    obj = IPWhois(ip)
    results = json.dumps(obj.lookup_whois(), indent=4)
    await ctx.send(results)

@bot.command()
async def uptime(ctx):
    await ctx.send("System uptime: " + get_uptime())

@bot.command()
async def xmas(ctx):
    currentdate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    xmasmsg = "There are %s days until Christmas!" % (days_to_xmas(datetime.datetime.strptime(currentdate, '%Y-%m-%d')))
    await ctx.send(xmasmsg)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello %s!" % ctx.message.author.mention)

bot.run(config.token)