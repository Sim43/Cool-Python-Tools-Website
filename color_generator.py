from PIL import Image
from collections import Counter, defaultdict

def rgb_to_hex(r, g, b):
    code = ('{:02X}' * 3).format(r, g, b)
    return '#' + code.lower()

def round_color(color, factor=5):
    """Round the RGB values to the nearest multiple of 'factor'."""
    return tuple((x // factor) * factor for x in color)

def generate_colors(loc, n_colors, factor=5):
    im = Image.open(loc)
    by_color = Counter()
    total_pixels = im.size[0] * im.size[1]

    for pixel in im.getdata():
        rounded_pixel = round_color(pixel, factor)  # Group similar colors
        by_color[rounded_pixel] += 1
    
    res = defaultdict(int)
    colors = by_color.most_common()
    for color_tuple, n_pixels in colors[:min(len(colors), n_colors)]:
        print(color_tuple)
        r, g, b = color_tuple[0], color_tuple[1], color_tuple[2]
        res[rgb_to_hex(r, g, b)] = round((n_pixels * 100) / total_pixels, 2)

    return dict(res)
