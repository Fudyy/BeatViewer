import disnake
from os import environ
from dotenv import load_dotenv
from disnake.ext import commands
from logger.logger import logger
from platform import python_version
import ossapi
from sys import exit

load_dotenv()

TOKEN = environ["TOKEN"]
OSU_ID = environ["OSU-ID"]
OSU_SECRET = environ["OSU-SECRET"]

if TOKEN is None:
    logger.error("No discord token provided on environment variables.")
    exit()

if OSU_ID is None or OSU_SECRET is None:
    logger.error("No osu oauth credentials provided on environment variables.")
    exit()

bot = commands.InteractionBot()
osu = ossapi.OssapiAsync(OSU_ID, OSU_SECRET, scopes=[ossapi.Scope.PUBLIC])

@bot.event
async def on_ready():
    logger.info("=" * 30)
    logger.info(f"Bot is running on client: {bot.user}")
    logger.info(f"Client ID: {bot.user.id}")
    logger.info(f"Python version: {python_version()}")
    logger.info(f"Disnake package version: {disnake.__version__}")
    logger.info("=" * 30)

bot.run(TOKEN)