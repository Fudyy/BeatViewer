import disnake
import ossapi
from os import environ
from dotenv import load_dotenv
from disnake.ext import commands
from logger.logger import logger
from platform import python_version
from sys import exit

load_dotenv()

TOKEN = environ["TOKEN"]
OSU_ID = environ["OSU-ID"]
OSU_SECRET = environ["OSU-SECRET"]
OSU_CALLBACK = environ["OSU-CALLBACK"]

if TOKEN is None:
    logger.error("No discord token provided on environment variables.")
    exit()

if OSU_ID is None or OSU_SECRET is None:
    logger.error("No osu oauth credentials provided on environment variables.")
    exit()

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(test_guilds=[1203814447295107152], intents=intents)
osu = ossapi.OssapiAsync(OSU_ID, OSU_SECRET, OSU_CALLBACK)

@bot.event
async def on_ready():
    logger.info("=" * 30)
    logger.info(f"Bot is running on client: {bot.user}")
    logger.info(f"Client ID: {bot.user.id}")
    logger.info(f"Python version: {python_version()}")
    logger.info(f"Disnake package version: {disnake.__version__}")
    logger.info("=" * 30)

    user = await osu.user("peppy")
    if user.id == 2:
        logger.info("Connected to Osu! api")
    else:
        logger.error("There was an error connecting to the osu! api")


bot.load_extension("cogs.map_listener")

bot.run(TOKEN)
