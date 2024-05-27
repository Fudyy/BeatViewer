from disnake.ext import commands
from disnake import Message
import re
from logger.logger import logger

class MapListener(commands.Cog):
    """Listens if a link of a mapset is sent on a message"""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.map_regex = r"https:\/\/osu\.ppy\.sh\/beatmapsets\/\d+#osu\/(\d+)"

    @commands.Cog.listener()
    async def on_message(self, message: Message):

        map_link = re.search(self.map_regex, message.content)
        
        if map_link:
            map_id = map_link.group(1)
            await message.reply(f"Mapa encontrado: {map_id}")

def setup(bot: commands.InteractionBot):
    bot.add_cog(MapListener(bot))
