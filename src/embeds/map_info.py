from disnake import Embed
from ossapi import Beatmapset, Beatmap

def create(map: Beatmap, mapset: Beatmapset = None):
    beatmapset = None
    if mapset:
        beatmapset = mapset
    else:
        beatmapset = map._beatmapset
    embed = Embed()

    embed.title = f"{beatmapset.artist} - {beatmapset.title}"
    embed.description = f"""
    **❤️ Favs: ``{beatmapset.favourite_count}`` | ▶️ Playcounts: ``{beatmapset.play_count}``**
     
    🟤 **{map.version}**
   
    **⭐ SR: ``{map.difficulty_rating}`` | ⌛Drain time: ``{map.drain}`` | 🎶 BPM: ``{beatmapset.bpm}``**
    """

    return embed