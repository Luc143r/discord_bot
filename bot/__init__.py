import discord
from discord.ext import commands
from config.config import PREFIX


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    initial_extensions = [
        'bot.commands.example_command', 'bot.events.on_message']
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'Loaded extension: {extension}')
        except Exception as e:
            print(f'Failed to load extension {extension}: {e}')
