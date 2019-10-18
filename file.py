import os
from PIL import Image, ImageDraw
from color import Color
import color

if __name__ == '__main__':

    # properties
    width = 25
    empty = 5
    div = color.Divider(60, zero=300)
    result_img = Image.new('RGB', (div.count() * 4, 12 * width + 10 * empty), 'gray')
    x, y = 0, 0

    # Normal color
    result: [int] = [1] * div.count()
    temp_img = Image.new('RGB', (div.count() * 4, width), 'gray')

    total = sum(result[:-2])
    draw = ImageDraw.Draw(result_img)
    temp_draw = ImageDraw.Draw(temp_img)
    for i in range(0, div.count() - 2):
        count = round(result[i] / total * result_img.size[0])
        while count > 0:
            for ind in range(0, width):
                print((x, y + ind))
                temp_draw.point((x, y + ind), fill=div.get_color_by_index(i).get_rgb_int())
                draw.point((x, y + ind), fill=div.get_color_by_index(i).get_rgb_int())

            count -= 1
            x += 1
    y += width + empty

    temp_img.save('./data/normal.jpg')

    # for years poster color
    for year in range(2008, 2019):
        x = 0
        result: [int] = [0] * div.count()
        temp_img = Image.new('RGB', (div.count() * 4, width), 'gray')

        for r, d, f in os.walk(f"./data/{year}"):
            for file in f:
                if not file.endswith(".jpg"):
                    continue
                im = Image.open(f"./data/{year}/{file}")
                print(f"opening ./data/{year}/{file}")
                pix = im.load()
                for j in range(0, im.size[1]):
                    for i in range(0, im.size[0]):
                        result[div.apply(Color.from_rgb_tuple(pix[i, j]))] += 1

        total = sum(result[:-2])
        draw = ImageDraw.Draw(result_img)
        temp_draw = ImageDraw.Draw(temp_img)
        for i in range(0, div.count() - 2):
            count = round(result[i] / total * result_img.size[0])
            while count > 0:
                for ind in range(0, width):
                    print((x, y + ind))
                    draw.point((x, y + ind), fill=div.get_color_by_index(i).get_rgb_int())
                    temp_draw.point((x, ind), fill=div.get_color_by_index(i).get_rgb_int())

                count -= 1
                x += 1
        y += width + empty

        temp_img.save(f'./data/t{year}.jpg')

    result_img.save('./data/test.jpg')
