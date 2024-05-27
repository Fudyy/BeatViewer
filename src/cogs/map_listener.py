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

        # search if the message have a beatmap link in it.
        match = re.search(self.map_regex, message.content)
        
        if match:
            set_id = match.group(1)
            map_id = match.group(2) if match.group(2) else None

            # if the link have an specified diff it shows it
            # example: https://osu.ppy.sh/beatmapsets/24313#osu/104229
            if map_id:
                try:
                    # it uses the beatmapset endpoit so it can get the language and genre info.
                    mapset = await osu.beatmapset(set_id)
                    beatmap = next((bm for bm in mapset.beatmaps if bm.id == int(map_id)), None)
                    # prevent to show a difficulty that doesn't exists (yeah i know that more than someone is gonna hard test the bot)
                    if beatmap:
                        await message.reply(embed=map_info.create(beatmap, mapset))
                    else:
                        return
                except:
                    pass
            # if the link only have the mapset id it uses the highest difficulty to show up
            # example: https://osu.ppy.sh/beatmapsets/24313
            else:
                try:
                    mapset = await osu.beatmapset(beatmapset_id=set_id)
                    beatmap = max(mapset.beatmaps, key=lambda b: b.difficulty_rating)
                    await message.reply(embed=map_info.create(beatmap, mapset))
                except:
                    pass
            

def setup(bot: commands.InteractionBot):
    bot.add_cog(MapListener(bot))
