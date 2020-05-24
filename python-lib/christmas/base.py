import argparse
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions


class SimpleBase(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("-r", "--led-rows", action="store",
                                 help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=32, type=int)
        self.parser.add_argument("-c", "--led-cols", action="store",
                                 help="Panel columns. Typically 32 or 64. (Default: 32)", default=64, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store",
                                 help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)

        self.parser.add_argument("-m", "--led-gpio-mapping",
                                 help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm",
                                 default='adafruit-hat', choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'],
                                 type=str)
        self.parser.add_argument("--led-slowdown-gpio", action="store",
                                 help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=2, type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store",
                                 help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130",
                                 default=130, type=int)
        self.parser.add_argument("--led-pwm-bits", action="store",
                                 help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)

        self.parser.add_argument("--led-scan-mode", action="store",
                                 help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)",
                                 default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true",
                                 help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument("--led-no-hardware-pulse", action="store",
                                 help="Don't use hardware pin-pulse generation")

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def run(self):
        print("Running")

    def process(self):
        self.args = self.parser.parse_args()

        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.pwm_bits = self.args.led_pwm_bits


        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.brightness = self.args.led_brightness

        if self.args.led_show_refresh:
            options.show_refresh_rate = 1
        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True

        self.matrix = RGBMatrix(options=options)

        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True
