from PIL import Image, ImageDraw, ImageFont
import shared

tile_size = 32
count = 0
row = 100
col = 40

font_file = "/home/sakkaku/Downloads/Retro Gaming.ttf"
font_size = 8
font = ImageFont.truetype(font_file, font_size)

OUTPUT = shared.output_dir(__file__)

for i in range(row):
    for j in range(col):
        img = Image.new(mode='RGB', size=(tile_size, tile_size), color='black')
        d = ImageDraw.Draw(img)
        text = str(count)
        left, top, right, bot = d.textbbox((0, 0), text, font=font)
        w = right - left
        h = bot - top
        h += int(h*0.21) # https://stackoverflow.com/questions/55773962/pillow-how-to-put-the-text-in-the-center-of-the-image

        d.text(((tile_size-w) / 2,(tile_size-h) / 2), text, font=font, fill='white')
        img.save(f'{OUTPUT}/{count}.png')

        count += 1