from disnake.ext import commands
from disnake import UserFlags, Embed, ApplicationCommandInteraction as Interaction
from ossapi import User
from main import osu
from unicodedata import lookup

class MapperInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="mapper",
                            description="Get information about a mapper")
    async def mapper_info(self, inter: Interaction, username: str = commands.Param(description="The mapper's username")):
        try:
            user = await osu.user(username)
        except:
            return await inter.response.send_message(f"User {username} not found.", ephemeral=True)
        
        await inter.response.send_message(embed=generate_embed(user))

def setup(bot):
    bot.add_cog(MapperInfo(bot))

def generate_embed(user: User):

    flag_unicode = [chr(0x1F1E6 + ord(char) - ord('A')) for char in user.country_code]

    embed = Embed(
        title = f"{''.join(flag_unicode)} {user.username}",
        url = f"https://osu.ppy.sh/users/{user.id}",
        description = f"""
        **Subs:** {user.mapping_follower_count} | **Kudosu:** {user.kudosu.total}
        """
    )

    embed.set_thumbnail(user.avatar_url)
    embed.set_image(user.cover_url)

    embed.set_author(name="Mapping profile for:")
    
    

    return embed