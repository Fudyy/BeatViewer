import re
from disnake.ext import commands
from disnake import Message, ui, ButtonStyle
from logger.logger import logger
from main import osu
from embeds import map_info
from ossapi import Beatmapset, Beatmap

class MapListener(commands.Cog):
    """
    Listens if a link of a beatmapset is sent on a message.
    if the link is sent it will send an embed with the information of the beatmapset.
    """

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.map_regex = r"https:\/\/osu\.ppy\.sh\/beatmapsets\/(\d+)(?:#\w+\/(\d+))?"

    @commands.Cog.listener()
    async def on_message(self, message: Message):

        # search if the message have a beatmap link in it.
        match = re.search(self.map_regex, message.content)
        
        if not match:
            return
            
        set_id = match.group(1)
        map_id = match.group(2) if match.group(2) else None

        # if the link have an specified diff it shows it
        # example: https://osu.ppy.sh/beatmapsets/24313#osu/104229
        if map_id:
            try:
                # it uses the beatmapset endpoit so it can get the language and genre info.
                mapset: Beatmapset = await osu.beatmapset(set_id)
                beatmap: Beatmap = next((bm for bm in mapset.beatmaps if bm.id == int(map_id)), None)
                # prevent to show a difficulty that doesn't exists (yeah i know that more than someone is gonna hard test the bot)
                if beatmap:
                    logger.info(f"Sending map info:  MAP ID: {beatmap.id} | CHANNEL: {message.channel.id}")
                    try:
                        await message.reply(embed=map_info.create(beatmap, mapset), view=BeatmapView(mapset, beatmap))
                    except Exception as e:
                        logger.error(f"There was an error sending the map info: {e}")
            except:
                pass
        # if the link only have the mapset id it uses the highest difficulty to show up
        # example: https://osu.ppy.sh/beatmapsets/24313
        else:
            try:
                mapset: Beatmapset = await osu.beatmapset(beatmapset_id=set_id)
                beatmap: Beatmap = max(mapset.beatmaps, key=lambda b: b.difficulty_rating)
                logger.info(f"Sending map info:  MAP ID: {beatmap.id} | CHANNEL: {message.channel.id}")
                try:
                    await message.reply(embed=map_info.create(beatmap, mapset), view=BeatmapView(mapset, beatmap))
                except Exception as e:
                    logger.error(f"There was an error sending the map info: {e}")
            except:
                pass

class BeatmapView(ui.View):
    def __init__(self, beatmapset: Beatmapset, beatmap: Beatmap):
        super().__init__()

        self.add_item(ui.Button(label="Map Info", style=ButtonStyle.url, url=beatmap.url))
        self.add_item(ui.Button(label="Map Discussion", style=ButtonStyle.url, url=f"https://osu.ppy.sh/beatmapsets/{beatmapset.id}/discussion"))

def setup(bot: commands.InteractionBot):
    bot.add_cog(MapListener(bot))
