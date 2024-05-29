from disnake.ext import commands

class ColorPaletteCommand(commands.Cog):
    """
    A cog that contains a command that sends a color palette image.
    """

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name="combo_colors")
    async def color_palette(self, ctx):
        """
        Sends a color palette from an image.
        """
        await ctx.send("test")

def setup(bot: commands.InteractionBot):
    bot.add_cog(ColorPaletteCommand(bot))