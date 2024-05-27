from disnake import Embed
from ossapi import Beatmapset, Beatmap, GameMode
from ossapi.enums import RankStatus
from main import osu

def create(map: Beatmap, mapset: Beatmapset = None):
    beatmapset = None
    if mapset:
        beatmapset = mapset
    else:
        beatmapset = map._beatmapset
    embed = Embed()

    # Drain time convertor
    minutes = map.hit_length // 60
    seconds = map.hit_length % 60
    formatted_drain_time = f"{minutes}:{seconds:02d}"

    embed.set_image(
        url=f"https://assets.ppy.sh/beatmaps/{beatmapset.id}/covers/cover@2x.jpg"
    )

    #Author section
    embed.set_author(
        name=f"Mapset by {beatmapset.creator}",
        url=f"https://osu.ppy.sh/users/{beatmapset.user_id}",
        icon_url=f"https://a.ppy.sh/{beatmapset.user_id}"
    )

    # Body section
    embed.title = f"{beatmapset.artist} - {beatmapset.title}"
    embed.url = map.url
    embed.description = f"""
    **❤️ Favs: ``{beatmapset.favourite_count}`` | ▶️ Playcounts: ``{beatmapset.play_count}``**
     
    🟤 **{map.version}**
   
    **⭐ SR: ``{map.difficulty_rating}`` | ⌛Drain time: ``{formatted_drain_time}`` | 🎶 BPM: ``{beatmapset.bpm}``**
    """
    # Fields section
    diff_settings_str = f"""
    AR: ``{map.ar}`` CS: ``{map.cs}``
    HP: ``{map.drain}`` OD: ``{map.accuracy}``
    """
    embed.add_field("Diff settings:", diff_settings_str, inline=True)
    embed.add_field("", "", inline=True)
    if beatmapset.source:
        embed.add_field("Source:", beatmapset.source, inline=True)
    else:
        embed.add_field("Source:", "Not specified", inline=True)

    embed.add_field("Genre:", beatmapset.genre, inline=True)
    embed.add_field("Language:", beatmapset.language, inline=True)

    if map.mode == GameMode.OSU:
        gamemode_name = "osu! standard"
    elif map.mode == GameMode.TAIKO:
        gamemode_name = "Taiko"
    elif map.mode == GameMode.CTB:
        gamemode_name = "Catch the Beat"
    elif map.mode == GameMode.MANIA:
        gamemode_name = "Mania"
    embed.add_field("Gamemode:", gamemode_name)

    # Footer
    if beatmapset.status == RankStatus.GRAVEYARD:
        status_text = "Graveyard"
    elif beatmapset.status == RankStatus.WIP:
        status_text = "WIP"
    elif beatmapset.status == RankStatus.PENDING:
        status_text = "Pending"
    elif beatmapset.status == RankStatus.RANKED:
        status_text = "Ranked"
    elif beatmapset.status == RankStatus.APPROVED:
        status_text = "Approved"
    elif beatmapset.status == RankStatus.QUALIFIED:
        status_text = "Qualified"
    elif beatmapset.status == RankStatus.LOVED:
        status_text = "Loved"
   
    embed.set_footer(
        text=f"Status: {status_text} | Last Updated"
    )

    embed.timestamp = beatmapset.last_updated

    return embed