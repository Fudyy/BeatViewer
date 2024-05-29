import io
from disnake import Attachment, Embed, File, ApplicationCommandInteraction as Interaction
from disnake.ext import commands
from PIL import Image, ImageDraw
from Pylette import extract_colors, Palette
from logger.logger import logger


class ComboColor(commands.Cog):
    """
    A cog that contains a command that sends a color palette image.
    """

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(name="combocolors",
                            description="Gets the color palette from an image to use as combo colors on a beatmap.",)
    async def combo_colors(self, 
                           ctx: Interaction, 
                           image: Attachment = commands.Param(description="The image to use, it must be a PNG/JPEG"), 
                           colors: int = commands.Param(default=4, 
                                                        description="The number of colors to extract from the image (10 max).")):
        """
        Gets the color palette from an image to use as combo colors on a beatmap.
        """
        if colors > 10:
            await ctx.send("The number of colors must be 10 or less.", ephemeral=True)
            return

        if image.content_type not in ["image/png", "image/jpeg"]:
            await ctx.send("The image must be a PNG or JPEG file.", ephemeral=True)
            return

        color_palette: Palette = extract_colors(
            image_url=image.url,
            palette_size=colors,
            resize=True,
            mode="MC",
            sort_mode="frequency"
        )

        palette_image = generate_palette_image(color_palette)
        image_byte_array = io.BytesIO()
        palette_image.save(image_byte_array, format="PNG")
        image_byte_array.seek(0)
        image_file = File(image_byte_array, filename="palette.png")
        await ctx.send(embed=Embed().set_image(file=image_file))


def setup(bot: commands.InteractionBot):
    bot.add_cog(ComboColor(bot))


def generate_palette_image(palette: Palette) -> Image.Image:
    """
    Generate an image containing the colors in the given palette.
    """
    image_width = 1000
    image_height = 532

    palette_size = len(palette.colors)

    img = Image.new("RGB", (1000, 532), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Draw the colors in the palette on the image

    if palette_size <= 5:
        color_width = image_width // palette_size
        color_height = image_height

        for i, color in enumerate(palette):
            draw.rectangle(
                [(i * color_width, 0), ((i + 1) * color_width, color_height)],
                fill=color.rgb
            )
    else:
        top_color_width = image_width // 5
        bottom_color_width = image_width // (palette_size - 5)

        color_height = image_height // 2

        for i, color in enumerate(palette):
            if i < 5:
                draw.rectangle(
                    [(i * top_color_width, 0), ((i + 1) * top_color_width, color_height)],
                    fill=color.rgb
                )
            else:
                draw.rectangle(
                    [((i - 5) * bottom_color_width, color_height), ((i - 4) * bottom_color_width, color_height * 2)],
                    fill=color.rgb
                )

    # TODO: Implement hitcircle generation

    return img

def generate_embed() -> Embed:
    # TODO
    pass


def generate_hitcircle(rgb_color: tuple, combo_number: int) -> Image.Image:
    hitcircle = Image.open(r"assets\hitcircle\hitcircle@2x.png")
    overlay = Image.open(r"assets\hitcircle\hitcircleoverlay@2x.png")
    img = hitcircle.convert("RGBA")

    # Iterate over each pixel in the image
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            # Get the pixel color
            r, g, b, a = img.getpixel((x, y))

            if a != 0:
                img.putpixel(
                    (x, y), (rgb_color[0], rgb_color[1], rgb_color[2], a))

    img.paste(overlay, (0, 0), mask=overlay)

    generate_number(combo_number, img)

    return img


def generate_number(combo_number: int, base_image: Image.Image) -> Image.Image:

    # Set numbers
    if combo_number != 10:
        # Opening the secondary image (overlay image)
        number_image = Image.open(
            rf"assets\hitcircle\default-{combo_number}@2x.png")

        # Get dimensions of each image
        width1, height1 = base_image.size
        width2, height2 = number_image.size

        # Find center pixel of outer image
        center_x, center_y = (width1//2), (height1//2)

        # Offset inner image to align its center
        im2_x = center_x - (width2//2)
        im2_y = center_y - (height2//2)

        # Pasting img2 image on top of img1
        base_image.paste(number_image, (im2_x, im2_y), mask=number_image)

        return base_image
    else:
        number_1 = Image.open(rf"assets\hitcircle\default-1@2x.png")
        number_0 = Image.open(rf"assets\hitcircle\default-0@2x.png")

        # Get dimensions of each image
        width1, height1 = base_image.size
        width2, height2 = number_1.size

        # Find center pixel of outer image
        center_x, center_y = (width1//2), (height1//2)

        # Offset inner image to align its center
        im2_x = center_x - (width2//2)
        im2_y = center_y - (height2//2)

        base_image.paste(number_1, (im2_x - 35, im2_y), mask=number_1)
        base_image.paste(number_0, (im2_x + 15, im2_y-1), mask=number_0)

        return base_image
    