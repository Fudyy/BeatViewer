import disnake
from os import environ
from dotenv import load_dotenv
from disnake.ext import commands
from logger.logger import logger
from platform import python_version

load_dotenv()

TOKEN = environ["TOKEN"]

bot = commands.InteractionBot()

@bot.event
async def on_ready():
    logger.info("=" * 30)
    logger.info(f"Bot is running on client: {bot.user}")
    logger.info(f"Client ID: {bot.user.id}")
    logger.info(f"Python version: {python_version()}")
    logger.info(f"Disnake package version: {disnake.__version__}")
    logger.info("=" * 30)

bot.run(TOKEN)