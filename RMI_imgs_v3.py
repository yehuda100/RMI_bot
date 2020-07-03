from PIL import Image
import random


def load():

    dot = Image.open("dot.png")
    design = Image.open("design.png")
    logo = Image.open("logo.png")
    banner = Image.open("banner.png")
    marks = Image.open("marks.png")
    water = Image.open("water.png")
    return dot, design, logo, banner, marks, water


def check_white(photo, image_size_x, image_size_y):

    photo_mat = photo.load()
    sum = 0
    r = 0
    g = 0
    b = 0
    for x in range(0, image_size_x, 40):
        for y in range(0, image_size_y // 5, 20):
            sum += 1
            r += photo_mat[x, y][0]
            g += photo_mat[x, y][1]
            b += photo_mat[x, y][2]
    return r // sum > 215 and g // sum > 215 and b // sum > 215


def paint(image, color, white_image=False):

    image = image.convert('RGBA')
    image_size_x, image_size_y = image.size
    image_mat = image.load()
    if white_image:
        for x in range(image_size_x):
            for y in range(image_size_y):
                if image_mat[x, y][0] > 200:
                    image_mat[x, y] = (80, 80, 80, image_mat[x, y][-1])
                elif image_mat[x, y][0] == 0:
                    image_mat[x, y] = color + (image_mat[x, y][-1],)
    else:
        for x in range(image_size_x):
            for y in range(image_size_y):
                if image_mat[x, y][0] == 0:
                    image_mat[x, y] = color + (image_mat[x, y][-1],)
    return image


def fix_size(image_size_x, image, image_name):

    ratio = {'dot': image_size_x//16, 'design': image_size_x//4, 'banner': image_size_x//2,\
    'marks': image_size_x//4, 'water': image_size_x//10*3}
    image.thumbnail((ratio[image_name], ratio[image_name]))
    return image


def produce_final(image, color, add, banner_offset):

    image_size_x, image_size_y = image.size
    final = Image.new('RGB', (image_size_x, image_size_y + add), (255, 255, 255))
    final.paste(image)

    dot, design, logo, banner, marks, water = load()

    white_image = check_white(image, image_size_x, image_size_y)

    colorize_dot = paint(dot, color)
    design = paint(design, color, white_image)
    banner = paint(banner, color)
    if white_image:
        color = (80, 80, 80)
    else:
        color = (255, 255, 255)
    non_colorize_dot = paint(dot, color, white_image)

    design.paste(logo, (1, 60), logo)

    colorize_dot = fix_size(image_size_x, colorize_dot, 'dot')
    non_colorize_dot = fix_size(image_size_x, non_colorize_dot, 'dot')
    design = fix_size(image_size_x, design, 'design')
    banner = fix_size(image_size_x, banner, 'banner')
    marks = fix_size(image_size_x, marks, 'marks')
    water = fix_size(image_size_x, water, 'water')

    counter = 0
    dot_size_x = colorize_dot.size[0]
    while counter < 16:
        if counter == 0:
            final.paste(colorize_dot, (dot_size_x * counter, 0), colorize_dot)
            counter = 1
        elif counter == 1:
            final.paste(design, (dot_size_x * counter, 0), design)
            counter = 5
        elif counter >= 5:
            if counter % 2 == 0:
                final.paste(non_colorize_dot, (dot_size_x * counter, 0), non_colorize_dot)
            else:
                final.paste(colorize_dot, (dot_size_x * counter, 0), colorize_dot)
            counter += 1

    final.paste(banner, (final.size[0] - banner_offset, image_size_y - (banner.size[1]//2)), banner)

    final_mat = final.load()
    for x in range(final.size[0]):
        for y in range(image_size_y + (banner.size[1]//5), image_size_y + (banner.size[1]//5) + 5):
            final_mat[x, y] = (0, 0, 0)

    marks = marks.convert('RGBA')
    final.paste(marks, (0, image_size_y - (marks.size[1]//2)), marks)
    final.paste(water, (0, final.size[1] - water.size[1]), water)

    return final


def bot(color, add_level, banner_level):
    colors = {
    'אדום': (255, 40, 40),
    'ירוק': (83, 198, 83),
    'כחול': (26, 117, 255),
    'זהב': (218, 165, 32),
    'כסף': (192, 192, 192),
    'טורקיז': (0, 200, 200),
    'סגול': (90, 30, 250),
    'עוד סגול': (198, 83, 140),
    'ברונזה': (205, 127, 50)}
    if color == 'אקראי':
        color = random.choice(((255, 40, 40), (83, 198, 83), (26, 117, 255),
                              (218, 165, 32), (192, 192, 192), (0, 200, 200),
                              (90, 30, 250), (198, 83, 140), (205, 127, 50)))
    else:
        color = colors[color]
    add_levels = {
    'הרבה': 3,
    'איפשהו באמצע': 2,
    'קצת': 1}
    add_level = add_levels[add_level]
    banner_levels = {
    'גדול': 1,
    'בינוני': 2,
    'קטן': 3}
    banner_level = banner_levels[banner_level]
    image = Image.open('photo.jpg')
    image_size_x, image_size_y = image.size
    add = image_size_y // 10 * (2 + (add_level % 4))
    banner_offset = (image_size_x // 4) + (image_size_x // 4) // (banner_level % 4)
    produce_final(image, color, add, banner_offset).save("final.jpg")
    return 'final'


def main():

    path = 'C:/Users/ybsh1/OneDrive/python/files/photo.jpg'
    image = Image.open(path)
    image.thumbnail((1280, 1280))
    image_size_x, image_size_y = image.size
    while image_size_x < 960:
        if image_size_x < 360:
            print(f'image size is {image_size_x}p - it\'s too small.')
        else:
            if input(f'image size is {image_size_x}p - are you sure you want to continue? (y/n) ') == 'y':
                break
        image = Image.open(path)
        image.thumbnail((1280, 1280))
        image_size_x, image_size_y = image.size

    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    add_level = 3#int(input('add level: '))
    add = image_size_y // 10 * (2 + add_level)
    banner_level = 2#int(input('banner level: '))
    banner_offset = (image_size_x // 4) + (image_size_x // 4) // banner_level
    text = """היי, מה נשמע?
איך המרגש והעניינים שבת שלום"""

    produce_final(image, color, add, banner_offset, text).save("C:/Users/ybsh1/OneDrive/python/files/final.jpg")

    print (color)


if __name__ == '__main__':
    main()

#By t.me/yehuda100
