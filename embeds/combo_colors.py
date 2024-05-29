from PIL import Image

def generate_hitcircle(rgb_color: tuple, combo_number: int):
    hitcircle = Image.open(r"assets\hitcircle\hitcircle@2x.png")
    overlay = Image.open(r"assets\hitcircle\hitcircleoverlay@2x.png")
    img = hitcircle.convert("RGBA")

    # Iterate over each pixel in the image
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            # Get the pixel color
            r, g, b, a = img.getpixel((x, y))

            if a != 0:
                img.putpixel((x, y), (rgb_color[0], rgb_color[1], rgb_color[2], a))

    img.paste(overlay, (0, 0), mask=overlay)

    generate_number(combo_number, img)

    return img


def generate_number(combo_number: int, base_image: Image.Image):

    # Set numbers
    if combo_number != 10:
        # Opening the secondary image (overlay image) 
        number_image = Image.open(rf"assets\hitcircle\default-{combo_number}@2x.png") 
        
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