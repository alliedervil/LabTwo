# Written with the help of Chat GPT4o

import time
import random
from neopixel import *

class NeoPixelController:

    def __init__(self, pin, num_pixels, brightness=0.2):
        """
        Initialize the NeoPixelController with the given pin, number of pixels, and brightness.
        """
        self._pin = pin
        self._num_pixels = num_pixels
        self._strip = Adafruit_NeoPixel(num_pixels, pin, 800000, 10, False, brightness)
        self._strip.begin()

    def set_pixel(self, index, color):
        """
        Set the color of a specific pixel.
        """
        self._strip.setPixelColor(index, color)
        self._strip.show()

    def set_all_pixels(self, color):
        """
        Set the color of all pixels.
        """
        for i in range(self._num_pixels):
            self._strip.setPixelColor(i, color)
        self._strip.show()

    def clear(self):
        """
        Clear all the pixels (set them to black/off).
        """
        self.set_all_pixels(Color(0, 0, 0))

    def show_pattern(self, colors, delay=50):
        """
        Show a pattern on the strip with the given colors and delay between changes.
        """
        for color in colors:
            self.set_all_pixels(color)
            time.sleep(delay / 1000.0)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """
        Display a rainbow cycle on the strip.
        """
        for j in range(256 * iterations):
            for i in range(self._num_pixels):
                self._strip.setPixelColor(i, self.wheel((i + j) & 255))
            self._strip.show()
            time.sleep(wait_ms / 1000.0)

    def wheel(self, pos):
        """
        Generate rainbow colors across 0-255 positions.
        """
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
