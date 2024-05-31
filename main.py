import disnake
import ossapi
from os import environ, listdir
from dotenv import load_dotenv
from disnake.ext import commands
from logger.logger import logger
from platform import python_version
from sys import exit

load_dotenv()

TOKEN = environ.get("TOKEN")
OSU_ID = environ.get("OSU-ID")
OSU_SECRET = environ.get("OSU-SECRET")
OSU_CALLBACK = environ.get("OSU-CALLBACK")

if TOKEN is None:
    logger.error("No discord token provided on environment variables.")
    exit()

if OSU_ID is None or OSU_SECRET is None:
    logger.error("No osu oauth credentials provided on environment variables.")
    exit()

intents = disnake.Intents.default()
intents.message_content = True
bot = commands.InteractionBot(test_guilds=[1203814447295107152, 1245122532030419017, 978827416237645824, 1244501835604037784], intents=intents)
osu = ossapi.OssapiAsync(OSU_ID, OSU_SECRET, OSU_CALLBACK)

@bot.event
async def on_ready():

    # Connect to the osu! api
    logger.info("Connecting to Osu! api...")
    user = await osu.user("peppy")
    if user.id == 2:
        logger.info("Successfully connected to the osu! api")
    else:
        logger.error("There was an error connecting to the osu! api")
        exit()
    
    # Log bot information
    logger.info("=" * 30)
    logger.info(f"Bot is running on client: {bot.user}")
    logger.info(f"Client ID: {bot.user.id}")
    logger.info(f"Python version: {python_version()}")
    logger.info(f"Disnake package version: {disnake.__version__}")
    logger.info("=" * 30)


def load_commands():
    try:
        commands_dir = listdir("cogs")
        logger.info("Started loading cogs")
        for file in commands_dir:
            if file.endswith(".py"):
                logger.info(f"Loading cog: {file[:-3]}")
                bot.load_extension(f"cogs.{file[:-3]}")
                logger.info(f"Successfully loaded cog: {file[:-3]}")
    except FileNotFoundError as err:
        logger.error(f"There was an error loading the cog: {err}")
        exit()

if __name__ == '__main__':
    load_commands()
    bot.run(TOKEN)
