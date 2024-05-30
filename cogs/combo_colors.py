import io
from typing import List
from disnake import Attachment, Embed, File, OptionChoice, Colour, ApplicationCommandInteraction as Interaction
from disnake.ext import commands
from PIL import Image, ImageDraw
from Pylette import extract_colors, Palette, Color
from logger.logger import logger


class ComboColor(commands.Cog):
    """
    A cog that contains a command that sends a color palette image.
    """

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(
        name="combocolors",
        description="Gets the color palette from an image to use as combo colors on a beatmap.",
    )
    async def combo_colors(
        self,
        ctx: Interaction,
        image: Attachment = commands.Param(description="The image to use, it must be a PNG/JPEG"),
        colors: int = commands.Param(
            default=4,
            description="The number of colors to extract from the image (10 max)."
        ),
        sort_mode: str = commands.Param(
            choices=[
                OptionChoice(name="Frequency", value="frequency"),
                OptionChoice(name="Luminance", value="luminance")
            ],
            default="frequency",
            name="sort_mode",
            description="The color sorting mode of the palette. (default: frequency)"
        ),
    ):
        """
        Gets the color palette from an image to use as combo colors on a beatmap.
        """
        if colors > 10:
            await ctx.send("The number of colors must be 10 or less.", ephemeral=True)
            return
        
        if colors < 1:
            await ctx.send("The number of colors must be 1 or more.", ephemeral=True)
            return

        if image.content_type not in ["image/png", "image/jpeg"]:
            await ctx.send("The image must be a PNG or JPEG file.", ephemeral=True)
            return

        logger.info(f"Requested color palette: USER: %s | CHANNEL: %s | IMAGE: %s", ctx.author.id, ctx.channel.id, image.url)

        try:
            generated_palette: Palette = extract_colors(
                image_url=image.url,
                palette_size=30,
                resize=True,
                mode="MC",
                sort_mode="frecuency"
            )

            # filter colors by ranking criteria luminance
            color_palette = filter_colors(generated_palette, colors)
            if len(color_palette) < colors:
                await ctx.send("The image does not contain enough colors to generate the requested palette (filtered by ranking criteria).", ephemeral=True)
                return
            
            # sort colors by luminance if requested
            if sort_mode == "luminance":
                color_palette.sort(key=lambda color: color.luminance)

            await ctx.send(embed=generate_embed(color_palette, image.url, sort_mode))
        except Exception as e:
            logger.error(f"Error generating color palette: %s", e)
            await ctx.send("An error occurred while generating the color palette. Please try again later.", ephemeral=True)


def setup(bot: commands.InteractionBot):
    bot.add_cog(ComboColor(bot))

def generate_embed(color_palette: Palette, original_image_url: str, sort_mode: str) -> Embed:
    """
    Generate an embed containing the color palette image.
    """

    embed = Embed(
        title="🎨 Combo Color Palette 🎨",
        color= Colour.from_rgb(color_palette[0].rgb[0], color_palette[0].rgb[1], color_palette[0].rgb[2]),
    )

    color_index = ""
    color_rgb = ""
    color_hex = ""

    for i, color in enumerate(color_palette):
        color_index += f"Color {i+1}: \n"
        color_rgb += f"{color.rgb[0]:<3}, {color.rgb[1]:<3}, {color.rgb[2]:<3}\n"
        color_hex += f"{rgb_to_hex(color.rgb)}\n"

    embed.add_field(name="Colors:", value=color_index, inline=True)
    embed.add_field(name="RGB:", value=color_rgb, inline=True)
    embed.add_field(name="Hex:", value=color_hex, inline=True)

    palette_image = generate_palette_image(color_palette)
    embed.set_image(file=palette_image)
    embed.set_thumbnail(url=original_image_url)

    embed.set_footer(text=f"Palette sorted by {sort_mode}")

    return embed

def rgb_to_hex(rgb: tuple) -> str:
    """
    Convert RGB color to hexadecimal color.
    """

    r, g, b = rgb
    hex_color = f"#{r:02x}{g:02x}{b:02x}"

    return hex_color

def filter_colors(generated_palette: Palette, colors: int) -> List[Color]:
    """
    Filter out colors that are too dark or too bright by ranking criteria.
    https://osu.ppy.sh/wiki/en/Ranking_criteria/osu! (section overall/guidelines)
    """
    color_palette: List[Color] = []
    for color in generated_palette.colors:
        luminance = color.luminance
        if luminance < 50 or luminance > 220:
            continue
        color_palette.append(color)
        if len(color_palette) == colors:
            break
    return color_palette

def generate_palette_image(palette: Palette) -> File:
    """
    Generate an image containing the colors in the given palette.
    """

    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 768

    # Hit circle image is 256x256!!

    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    palette_size = len(palette)

    if palette_size <= 5:
        color_width = round(IMAGE_WIDTH / palette_size)
        color_height = IMAGE_HEIGHT

        for i, color in enumerate(palette):
            x_start = i * color_width
            x_end = (i + 1) * color_width

            draw.rectangle([(x_start, 0), (x_end, color_height)], fill=color.rgb)

            hitcircle = generate_hitcircle(color.rgb, i+1)

            color_center = x_start + color_width // 2
            img.paste(hitcircle, (color_center - 128, (color_height//3)), mask=hitcircle)

    # If the palette has more than 5 colors, draw the first 5 colors on the top half of the image and the rest on the bottom half
    else:
        top_color_width = IMAGE_WIDTH // 5
        bottom_color_width = round(IMAGE_WIDTH / (palette_size - 5))

        color_height = IMAGE_HEIGHT // 2

        for i, color in enumerate(palette):
            if i < 5:
                # TOP HALF
                x_start = i * top_color_width
                x_end = (i + 1) * top_color_width

                draw.rectangle([(x_start, 0), (x_end, color_height)], fill=color.rgb)

                hitcircle = generate_hitcircle(color.rgb, i+1)

                color_center = x_start + top_color_width // 2
                img.paste(hitcircle, (color_center - 128, (color_height // 2) - 128), mask=hitcircle)
            else:
                # BOTTOM HALF
                x_start = (i - 5) * bottom_color_width
                x_end = (i - 4) * bottom_color_width

                draw.rectangle([(x_start, color_height), (x_end, color_height * 2)], fill=color.rgb)

                hitcircle = generate_hitcircle(color.rgb, i+1)

                color_center = x_start + bottom_color_width // 2
                img.paste(hitcircle, (color_center - 128, ((color_height // 2) * 3) - 128), mask=hitcircle)

    # Save the image to a disnake File object
    image_byte_array = io.BytesIO()
    img.save(image_byte_array, format="PNG")
    image_byte_array.seek(0)
    image_file = File(image_byte_array, filename="palette.png")

    return image_file

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
    