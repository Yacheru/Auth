import json
import discord
import dotenv
import os
from discord.ext import commands

with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(f"{cfg['BOT']['prefix']}"),
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=2, name="https://yacheru.ru/login"),
    help_command=None)

@bot.event
async def on_ready():
    for f in os.listdir("main/cogs"):
        if f.endswith(".py"):
            await bot.load_extension(f"cogs.{f[:-3]}")

dotenv.load_dotenv()
TOKEN = cfg['BOT']['TOKEN']