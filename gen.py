from PIL import Image, ImageDraw

import color

if __name__ == '__main__':

    width = 25
    empty = 5

    div = color.Divider(60, zero=300)
    result_img = Image.new('RGB', (div.count() * 4, width), 'gray')
    y = 0

    x = 0
    result: [int] = [1] * div.count()

    total = sum(result[:-2])
    draw = ImageDraw.Draw(result_img)
    for i in range(0, div.count() - 2):
        count = round(result[i] / total * result_img.size[0])
        while count > 0:
            for ind in range(0, width):
                print((x, y + ind))
                draw.point((x, y + ind), fill=div.get_color_by_index(i).get_rgb_int())

            count -= 1
            x += 1

    result_img.save('./data/normal.jpg')
