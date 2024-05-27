from disnake import Embed
from ossapi import Beatmapset, Beatmap, GameMode
from ossapi.enums import RankStatus
from main import osu

def create(map: Beatmap, beatmapset: Beatmapset):

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
     
    {get_emoji(map.difficulty_rating, map.mode)} **{map.version}**
   
    **⭐ SR: ``{map.difficulty_rating}`` | ⌛Drain time: ``{formatted_drain_time}`` | 🎶 BPM: ``{beatmapset.bpm}``**
    """

    # Fields section
    # diff settings
    diff_settings_str = f"""
    AR: ``{map.ar}`` CS: ``{map.cs}``
    HP: ``{map.drain}`` OD: ``{map.accuracy}``
    """
    embed.add_field("Diff settings:", diff_settings_str, inline=True)

    # Nominators
    if beatmapset.current_nominations:
        nominators = []
        for nomination in beatmapset.current_nominations:
            for related_user in beatmapset.related_users:
                if related_user["id"] == nomination.user_id:
                    nominators.append(related_user["username"])

        embed.add_field("Nominators:", ", ".join(nominators), inline=True)
    else:
        embed.add_field("", "", inline=True)


    if beatmapset.source:
        embed.add_field("Source:", beatmapset.source, inline=True)
    else:
        embed.add_field("Source:", "Unspecified", inline=True)

    embed.add_field("Genre:", beatmapset.genre["name"], inline=True)
    embed.add_field("Language:", beatmapset.language["name"], inline=True)

    if map.mode == GameMode.OSU:
        gamemode_name = "osu!"
    elif map.mode == GameMode.TAIKO:
        gamemode_name = "Taiko"
    elif map.mode == GameMode.CATCH:
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

def get_emoji(difficulty_rating: float, gamemode: GameMode):
    emojis = []
    if gamemode == GameMode.OSU:
        emojis = [
            "<:std_1:1244766827134058636>", 
            "<:std_2:1244766789217419284>", 
            "<:std_3:1244766788261253140>", 
            "<:std_4:1244766787174793237>", 
            "<:std_5:1244766785216188499>", 
            "<:std_6:1244766784503025835>", 
            "<:std_7:1244766783160717353>", 
            "<:std_8:1244766781889974323>", 
            "<:std_9:1244766780447264808>"
        ]
    elif gamemode == GameMode.TAIKO:
        emojis = [
            "<:taiko_1:1244775746497679391>",
            "<:taiko_2:1244775734862417981>",
            "<:taiko_3:1244775732836569130>",
            "<:taiko_4:1244775731678941284>",
            "<:taiko_5:1244775730546737163>",
            "<:taiko_6:1244775729057497098>",
            "<:taiko_7:1244775727635632138>",
            "<:taiko_8:1244775726411026512>",
            "<:taiko_9:1244775724993220680>"
        ]
    elif gamemode == GameMode.CATCH:
        emojis = [
            "<:ctb_1:1244774445109870633>",
            "<:ctb_2:1244774423677112381>",
            "<:ctb_3:1244774422615687338>",
            "<:ctb_4:1244774421407994019>",
            "<:ctb_5:1244774419768016937>",
            "<:ctb_6:1244774418530439251>",
            "<:ctb_7:1244774417683316818>",
            "<:ctb_8:1244774416441802882>",
            "<:ctb_9:1244774415149830226>"
        ]
    elif gamemode == GameMode.MANIA:
        emojis = [
            "<:mania_1:1244775165880045618>", 
            "<:mania_2:1244775149404946474>",
            "<:mania_3:1244775148335141044>", 
            "<:mania_4:1244775146879713302>", 
            "<:mania_5:1244775145822879824>", 
            "<:mania_6:1244775144765919344>", 
            "<:mania_7:1244775143008505937>", 
            "<:mania_8:1244775141934759988>", 
            "<:mania_9:1244775140802297987>"
        ]


    if difficulty_rating >= 9:
        return emojis[-1]
    return emojis[int(difficulty_rating)-1]