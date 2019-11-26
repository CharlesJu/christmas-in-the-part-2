import time
from PIL import Image
from base import SimpleBase
import argparse

parser = argparse.ArgumentParser()

# parser.add_argument()

def scroll_image(base: SimpleBase, image_path: str, scroll_speed: float):
    image = Image.open(image_path).convert('RGB')
    image.resize((base.matrix.width, base.matrix.height), Image.ANTIALIAS)

    double_buffer = base.matrix.CreateFrameCanvas()
    width, height = image.size

    for xpos in range(width):
        double_buffer.SetImage(image, -xpos)
        double_buffer.SetImage(image, -xpos + width)
        double_buffer = base.matrix.SwapOnVSync(double_buffer)
        time.sleep(scroll_speed)


if __name__ == "__main__":
    base = SimpleBase()
    scroll_image(base, "feelsgoodman.ppm", 0.01)

