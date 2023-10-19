import sys
sys.dont_write_bytecode = True

from bot import bot, TOKEN
from main.verif import *

bot.run(TOKEN)
