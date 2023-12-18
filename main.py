import os
from dotenv import load_dotenv
from bot import bot


load_dotenv()

bot.run(os.getenv('token'))
