from disnake import Attachment, ApplicationCommandInteraction as Interaction
from disnake.ext import commands
from PIL import Image, ImageDraw2

class ColorPaletteCommand(commands.Cog):
    """
    A cog that contains a command that sends a color palette image.
    """

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name="combocolors",
                            description="Gets the color palette from an image to use as combo colors on a beatmap.",)
    async def combo_colors(self, ctx: Interaction, image: Attachment):
        """
        Gets the color palette from an image to use as combo colors on a beatmap.
        """
        # Check if the image is a PNG or JPEG file.
        if image.content_type not in ["image/png", "image/jpeg"]:
            await ctx.send("The image must be a PNG or JPEG file.")
            return

        await ctx.send("enviaste una imagen!")

def setup(bot: commands.InteractionBot):
    bot.add_cog(ColorPaletteCommand(bot))