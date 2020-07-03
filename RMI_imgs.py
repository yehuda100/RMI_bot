from PIL import Image, ImageDraw, ImageFont
import random


def add_text(text, image_size_x):
    text = text.splitlines()
    image = Image.new('RGB', (image_size_x, image_size_x), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font_size = (image_size_x - image_size_x // 5) // 13
    font = ImageFont.truetype('Ahlab.ttf', font_size)
    new_line_list = []
    for line in text:
        if draw.textsize(line, font=font)[0] > image_size_x - image_size_x // 5:
            lines = line.split()
            while len(lines) > 0:
                new_line = lines.pop(0)
                while draw.textsize(new_line, font=font)[0] < image_size_x - image_size_x // 5:
                    if len(lines) > 0:
                        new_line += ' ' + lines.pop(0)
                    else:
                        break
                new_line_list.append(new_line[::-1])
        else:
            new_line_list.append(line[::-1])

    text = '\n'.join(new_line_list)
    text_size = draw.multiline_textsize(text, font=font)
    draw.multiline_text(((image_size_x - text_size[0]) // 2, image_size_x // 10), text, fill='black', font=font, align='right')
    return image, text_size


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


def fix_size(scale, image, image_name):

    ratio = {'dot': scale // 16, 'design': scale // 4, 'banner': scale // 2,\
    'marks': scale // 4, 'water': scale // 10 * 3}
    image.thumbnail((ratio[image_name], ratio[image_name]))
    return image


def banner_text(banner, quoted):
    banner_size = banner.size
    draw = ImageDraw.Draw(banner)
    quoted = '{:^10}'.format(quoted[::-1])
    font_size = 72
    font = ImageFont.truetype('Agas.ttf', font_size)
    quoted_size = draw.textsize(quoted, font=font)
    while quoted_size[0] > banner_size[0] - banner_size[0] // 5 or quoted_size[1] > round(banner_size[1] / 1.4):
        font_size -= 4
        font = ImageFont.truetype('Agas.ttf', font_size)
        quoted_size = draw.textsize(quoted, font=font)
    banner = banner.crop((0, 0, quoted_size[0] + banner_size[0] // 6, banner_size[1]))
    draw = ImageDraw.Draw(banner)
    banner_size = banner.size
    draw.text(((banner_size[0] - quoted_size[0]) // 2 + banner_size[0] // 20, (banner_size[1] - quoted_size[1]) // 2 - banner_size[1] // 7), quoted, fill='white', font=font)
    return banner


def produce_final(image, color, text, quoted):

    image_size_x, image_size_y = image.size
    text_image, text_size = add_text(text, image_size_x)

    final = Image.new('RGB', (image_size_x, image_size_y + text_size[1] + image_size_x // 5), (255, 255, 255))
    final.paste(image)
    final.paste(text_image, (0, image_size_y))

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

    if image_size_x > image_size_y:
        scale = image_size_y
    else:
        scale = image_size_x

    colorize_dot = fix_size(scale, colorize_dot, 'dot')
    non_colorize_dot = fix_size(scale, non_colorize_dot, 'dot')
    design = fix_size(scale, design, 'design')
    banner = fix_size(image_size_x, banner, 'banner')
    marks = fix_size(image_size_x, marks, 'marks')
    water = fix_size(image_size_x, water, 'water')

    counter = 0
    dot_size_x = colorize_dot.size[0]
    while counter * dot_size_x < image_size_x - dot_size_x:
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

    banner = banner_text(banner, quoted)
    banner_size = banner.size
    final.paste(banner, (image_size_x - banner_size[0], image_size_y - banner_size[1]//2), banner)

    final_mat = final.load()
    for x in range(image_size_x):
        for y in range(image_size_y + (banner_size[1]//5), image_size_y + (banner_size[1]//5) + banner_size[1]//20):
            final_mat[x, y] = (0, 0, 0)

    marks = marks.convert('RGBA')
    final.paste(marks, (0, image_size_y - (marks.size[1]//2)), marks)
    final.paste(water, (0, final.size[1] - water.size[1]), water)

    return final


def bot(data):
    file_name, color, text, qouted = data
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
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    else:
        color = colors[color]

    image = Image.open('{}.jpg'.format(file_name))
    produce_final(image, color, text, qouted).save('final{}.jpg'.format(file_name))
    return 'final{}'.format(file_name)


def get_size(image):
    return Image.open(image).size[0]


def main():

    image = Image.open('C:/Users/ybsh1/OneDrive/python/files/photo.jpg')
    image.thumbnail((1280, 1280))

    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    text = 'סרחיו שייך לכאן.\n הוא איתנו כבר מלא ש\nנים והוא צריך לפרוש כאן. זה מה שאני חושב ואני אעמוד על כך.'
    quoted = 'פלורנטינו פרס'
    quoted2 = 'אני'
    quoted3 = 'כריסטןליאנו'

    produce_final(image, color, text, quoted).show()

if __name__ == '__main__':
    main()

#By t.me/yehuda100