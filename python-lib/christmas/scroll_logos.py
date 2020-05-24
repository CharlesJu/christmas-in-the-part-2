import time
from PIL import Image
from base import SimpleBase
import argparse
import glob
import os
from rgbmatrix import graphics
import math

# parser = argparse.ArgumentParser()
#
# parser.add_argument("-f", "--folder", help="The image folder to display", type=str)

def rotate_block(base, rotations):
    def rotate(x, y, angle):
        return {
            "new_x": x * math.cos(angle) - y * math.sin(angle),
            "new_y": x * math.sin(angle) + y * math.cos(angle)
        }
    def scale_col(val, lo, hi):
        if val < lo:
            return 0
        if val > hi:
            return 255
        return 255 * (val - lo) / (hi - lo)

    cent_x = base.matrix.width / 2
    cent_y = base.matrix.height / 2

    rotate_square = min(base.matrix.width, base.matrix.height) * 1.41
    min_rotate = cent_x - rotate_square / 2
    max_rotate = cent_x + rotate_square / 2

    display_square = min(base.matrix.width, base.matrix.height) * 0.7
    min_display = cent_x - display_square / 2
    max_display = cent_x + display_square / 2

    deg_to_rad = 2 * 3.14159265 / 360
    rotation = 0
    offset_canvas = base.matrix.CreateFrameCanvas()
    rot = 0
    while rot < rotations * 360:
        rot += 1
        rotation += 1
        rotation %= 360

        for x in range(int(min_rotate), int(max_rotate)):
            for y in range(int(min_rotate), int(max_rotate)):
                ret = rotate(x - cent_x, y - cent_x, deg_to_rad * rotation)
                rot_x = ret["new_x"]
                rot_y = ret["new_y"]

                if x >= min_display and x < max_display and y >= min_display and y < max_display:
                    offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, scale_col(x, min_display, max_display), 255 - scale_col(y, min_display, max_display), scale_col(y, min_display, max_display))
                else:
                    offset_canvas.SetPixel(rot_x + cent_x, rot_y + cent_y, 0, 0, 0)

        offset_canvas = base.matrix.SwapOnVSync(offset_canvas)

def scroll_image(base: SimpleBase, image_path: str, scroll_speed: float):
    image = Image.open(image_path).convert('RGB')
    # image = image.resize((base.matrix.width, base.matrix.height), Image.ANTIALIAS)
    # print(image)
    double_buffer = base.matrix.CreateFrameCanvas()
    width, height = image.size

    for xpos in range(64, -width, -1):
        double_buffer.SetImage(image, xpos)
        # double_buffer.SetImage(image, -xpos + width)
        double_buffer = base.matrix.SwapOnVSync(double_buffer)
        time.sleep(scroll_speed)

def scroll_folder(base: SimpleBase, folder: str, scroll_speed: float):
    files = glob.glob(os.path.join(folder, '*.ppm'))
    images = [ Image.open(x).convert('RGB').resize((base.matrix.width, base.matrix.height), Image.ANTIALIAS) for x in files ]
    widths, heights = zip(*(i.size for i in images ))
    total_width = sum(widths)
    max_height = max(heights)
    full_im = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for im in images:
        full_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    double_buffer = base.matrix.CreateFrameCanvas()
    width, height = full_im.size

    for xpos in range(width, -width, -1):
        double_buffer.SetImage(full_im, xpos)
        # double_buffer.SetImage(image, -xpos + width)
        double_buffer = base.matrix.SwapOnVSync(double_buffer)
        time.sleep(scroll_speed)
def show_image(base, file, show_time):
    image = Image.open(file).convert('RGB')
    image = image.resize((base.matrix.width, base.matrix.height), Image.ANTIALIAS)
    # print(image)
    double_buffer = base.matrix.CreateFrameCanvas()
    width, height = image.size
    double_buffer.SetImage(image, 0)
    double_buffer = base.matrix.SwapOnVSync(double_buffer)
    time.sleep(show_time)

def run_text(base, text):
    offscreen_canvas = base.matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("/home/pi/fonts/7x13.bdf")
    textColor = graphics.Color(255,0,0)
    offscreen_canvas.Clear()
    pos = offscreen_canvas.width
    len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, text)
    # print(pos)
    while pos > -(offscreen_canvas.width + 64):
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, pos, 20, textColor, text)
        pos -= 1
        # if (pos + len < 0):
        #     pos = offscreen_canvas.width

        time.sleep(0.05)
        offscreen_canvas = base.matrix.SwapOnVSync(offscreen_canvas)

if __name__ == "__main__":
    # args = parser.parse_args()
    #
    # folder = args.folder
    base = SimpleBase()

    if (not base.process()):
        base.print_help()
    while True:
        show_image(base, "/home/pi/holidays.ppm", 5)
        rotate_block(base, 0.25)
        run_text(base, "#SCUEngineering")
        scroll_image(base, "/home/pi/full_scroll_final.ppm", 0.04)
        rotate_block(base, 0.25)
        show_image(base, "/home/pi/1heart.ppm", 0.5)
        show_image(base, "/home/pi/2heart.ppm", 0.5)
        show_image(base, "/home/pi/3heart.ppm", 0.5)
        show_image(base, "/home/pi/4heart.ppm", 0.5)
        show_image(base, "/home/pi/1heart.ppm", 0.5)
        show_image(base, "/home/pi/2heart.ppm", 0.5)
        show_image(base, "/home/pi/3heart.ppm", 0.5)
        show_image(base, "/home/pi/4heart.ppm", 0.5)
        show_image(base, "/home/pi/1heart.ppm", 0.5)
        show_image(base, "/home/pi/2heart.ppm", 0.5)
        show_image(base, "/home/pi/3heart.ppm", 0.5)
        show_image(base, "/home/pi/4heart.ppm", 0.5)
        rotate_block(base, 0.25)
