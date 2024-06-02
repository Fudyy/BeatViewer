from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Interaction
from main import osu

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
        
        await inter.response.send_message(f"Getting information about {user.username}...")

def setup(bot):
    bot.add_cog(MapperInfo(bot))