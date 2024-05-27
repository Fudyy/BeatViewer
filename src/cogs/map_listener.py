from disnake.ext import commands
from disnake import Message
import re
from logger.logger import logger
from main import osu
from embeds import map_info

class MapListener(commands.Cog):
    """Listens if a link of a beatmapset is sent on a message"""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.map_regex = r"https:\/\/osu\.ppy\.sh\/beatmapsets\/(\d+)(?:#\w+\/(\d+))?"

    @commands.Cog.listener()
    async def on_message(self, message: Message):

        match = re.search(self.map_regex, message.content)
        
        if match:
            set_id = match.group(1)
            map_id = match.group(2) if match.group(2) else None
            beatmap = None
            if map_id:
                beatmap = await osu.beatmap(map_id)
                await message.reply(embed=map_info.create(beatmap))
            else:
                mapset = await osu.beatmapset(set_id)
                beatmap = max(mapset.beatmaps, key=lambda b: b.difficulty_rating)
                await message.reply(embed=map_info.create(beatmap, mapset=mapset))
            

def setup(bot: commands.InteractionBot):
    bot.add_cog(MapListener(bot))
