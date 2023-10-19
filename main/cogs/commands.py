import discord
from discord.ext import commands
from bot import bot

class Commands(commands.Cog):
    def __init__(self, bot = commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self,):
        print("Bot is Ready!")

    @commands.command()
    @commands.has_guild_permissions(administrator = True)
    async def ping(self, ctx: commands.Context):
        print(f"Сообщение от {ctx.author.name} в канале {ctx.channel.name}")

def setup(bot: commands.Bot):
    bot.add_cog(Commands(bot))
    print(f"Ког {__name__} запущен")