from disnake import Embed, Colour
from ossapi import Beatmapset, Beatmap, GameMode
from ossapi.enums import RankStatus
from Pylette import extract_colors, Color

def create(map: Beatmap, beatmapset: Beatmapset) -> Embed:
    embed = Embed()

    # Convert drain time to minutes and seconds
    minutes = map.hit_length // 60
    seconds = map.hit_length % 60
    formatted_drain_time = f"{minutes}:{seconds:02d}"

    # Set the cover image for the embed
    embed.set_image(url=f"https://assets.ppy.sh/beatmaps/{beatmapset.id}/covers/cover@2x.jpg")

    # Set the thumbnail image for the embed
    embed.set_thumbnail(url=f"https://a.ppy.sh/{beatmapset.user_id}")

    # Extract and set the dominant color from the cover image
    bg_color_extract: Color = extract_colors(
        image_url=f"https://assets.ppy.sh/beatmaps/{beatmapset.id}/covers/cover@2x.jpg",
        palette_size=10,
        resize=True,
        mode="MC"
    )[0]
    
    bg_color = Colour.from_rgb(int(bg_color_extract.rgb[0]), int(bg_color_extract.rgb[1]), int(bg_color_extract.rgb[2]))
    embed.color = bg_color

    # Set the author section of the embed
    embed.set_author(
        name=f"Mapset by {beatmapset.creator}",
        url=f"https://osu.ppy.sh/users/{beatmapset.user_id}",
        icon_url=f"https://a.ppy.sh/{beatmapset.user_id}"
    )

    # Set the title, URL, and description of the embed
    embed.title = f"{beatmapset.artist} - {beatmapset.title}"
    embed.url = map.url
    embed.description = (
        f"**❤️ Favs: ``{beatmapset.favourite_count}`` | ▶️ Playcounts: ``{beatmapset.play_count}``**\n\n"
        f"{get_diff_emoji(map.difficulty_rating, map.mode)} **{map.version}** ``{map.difficulty_rating}`` ⭐\n\n"
        f"**⏱️ Drain time: ``{formatted_drain_time}`` | 🎶 BPM: ``{beatmapset.bpm}``**"
    )

    # Add field for difficulty settings
    diff_settings_str = (
        f"AR: ``{map.ar}`` \n"
        f"CS: ``{map.cs}`` \n"
        f"HP: ``{map.drain}`` \n"
        f"OD: ``{map.accuracy}``"
    )
    embed.add_field(name="Diff settings:", value=diff_settings_str, inline=True)

    # Add field for nominators if any
    if beatmapset.current_nominations:
        nominators = []
        for nomination in beatmapset.current_nominations:
            for related_user in beatmapset.related_users:
                if related_user["id"] == nomination.user_id:
                    nominators.append(related_user["username"])
        embed.add_field(name="Nominators:", value=", ".join(nominators), inline=True)
    else:
        embed.add_field(name="Nominators:", value="None", inline=True)

    # Add field for source if specified
    source = beatmapset.source if beatmapset.source else "Unspecified"
    embed.add_field(name="Source:", value=source, inline=True)

    # Add fields for genre and language
    embed.add_field(name="Genre:", value=beatmapset.genre["name"], inline=True)
    embed.add_field(name="Language:", value=beatmapset.language["name"], inline=True)

    # Determine and add the game mode field
    gamemode_name = {
        GameMode.OSU: "osu!",
        GameMode.TAIKO: "Taiko",
        GameMode.CATCH: "Catch the Beat",
        GameMode.MANIA: "Mania"
    }.get(map.mode, "Unknown")
    embed.add_field(name="Gamemode:", value=gamemode_name, inline=True)

    # Determine and set the footer based on the beatmap status
    map_status = {
        RankStatus.GRAVEYARD: "Graveyard",
        RankStatus.WIP: "WIP",
        RankStatus.PENDING: "Pending",
        RankStatus.RANKED: "Ranked",
        RankStatus.APPROVED: "Approved",
        RankStatus.QUALIFIED: "Qualified",
        RankStatus.LOVED: "Loved"
    }.get(beatmapset.status, "Unknown")

    embed.set_footer(text=f"Status: {map_status} | Last Updated")
    embed.timestamp = beatmapset.last_updated

    return embed


from ossapi import GameMode

def get_diff_emoji(difficulty_rating: float, gamemode: GameMode) -> str:
    # Dictionary to map game modes to their corresponding emoji lists
    emojis = {
        GameMode.OSU: [
            "<:std_1:1244766827134058636>", 
            "<:std_2:1244766789217419284>", 
            "<:std_3:1244766788261253140>", 
            "<:std_4:1244766787174793237>", 
            "<:std_5:1244766785216188499>", 
            "<:std_6:1244766784503025835>", 
            "<:std_7:1244766783160717353>", 
            "<:std_8:1244766781889974323>", 
            "<:std_9:1244766780447264808>"
        ],
        GameMode.TAIKO: [
            "<:taiko_1:1244775746497679391>",
            "<:taiko_2:1244775734862417981>",
            "<:taiko_3:1244775732836569130>",
            "<:taiko_4:1244775731678941284>",
            "<:taiko_5:1244775730546737163>",
            "<:taiko_6:1244775729057497098>",
            "<:taiko_7:1244775727635632138>",
            "<:taiko_8:1244775726411026512>",
            "<:taiko_9:1244775724993220680>"
        ],
        GameMode.CATCH: [
            "<:ctb_1:1244774445109870633>",
            "<:ctb_2:1244774423677112381>",
            "<:ctb_3:1244774422615687338>",
            "<:ctb_4:1244774421407994019>",
            "<:ctb_5:1244774419768016937>",
            "<:ctb_6:1244774418530439251>",
            "<:ctb_7:1244774417683316818>",
            "<:ctb_8:1244774416441802882>",
            "<:ctb_9:1244774415149830226>"
        ],
        GameMode.MANIA: [
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
    }

    # Get the appropriate emoji list for the given game mode
    mode_emojis = emojis.get(gamemode, [])

    # If the difficulty rating is 9 or higher, return the highest emoji
    if difficulty_rating >= 9:
        return mode_emojis[-1]

    # Otherwise, return the emoji corresponding to the difficulty rating
    return mode_emojis[int(difficulty_rating)-1]
