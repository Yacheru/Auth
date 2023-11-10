import json
import discord
import dotenv
from discord.ext import commands

with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(f"{cfg['BOT']['prefix']}"),
    intents=discord.Intents.all(),
    activity=discord.Activity(
        type=2, name="https://yacheru.ru/login"),
    help_command=None)

dotenv.load_dotenv()
TOKEN = cfg['BOT']['TOKEN']
