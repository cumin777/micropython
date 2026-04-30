# test_neopixel.py
# Test WS2812B RGB LED (GPIO12) with power control (GPIO24) on XIAO RP2040 Plus
# No external hardware needed - uses onboard RGB LED.
# Requires ws2812.py library (from Seeed Studio) to be on the board filesystem.
#
# Usage:
#   1. Upload ws2812.py to the board first
#   2. Then run this test: import test_neopixel

from machine import Pin
from ws2812 import WS2812
import time

# WS2812 pins
NEOPIXEL_DATA = 12    # GPIO12
NEOPIXEL_POWER = 24   # GPIO24 (active high)
NUM_LEDS = 1          # Single onboard WS2812

# Power pin (keep as global to prevent GC resetting it)
_pwr = Pin(NEOPIXEL_POWER, Pin.OUT)


def power_on():
    """Enable WS2812 power."""
    _pwr.value(1)
    time.sleep_ms(50)  # Wait for power to stabilize


def power_off():
    """Disable WS2812 power."""
    _pwr.value(0)


def test_neopixel_colors():
    """Cycle through basic colors."""
    print("=== WS2812 RGB LED Color Test ===")
    print("Data=GPIO12, Power=GPIO24")

    power_on()

    # Create WS2812 instance after power is on
    led = WS2812(NEOPIXEL_DATA, NUM_LEDS, brightness=1.0)

    colors = [
        (255, 0, 0, "Red"),
        (0, 255, 0, "Green"),
        (0, 0, 255, "Blue"),
        (255, 255, 0, "Yellow"),
        (0, 255, 255, "Cyan"),
        (255, 0, 255, "Magenta"),
        (255, 255, 255, "White"),
        (0, 0, 0, "Off"),
    ]

    for r, g, b, name in colors:
        led.pixels_fill((r, g, b))
        led.pixels_show()
        print("  Color: {} (R={}, G={}, B={})".format(name, r, g, b))
        time.sleep(1)

    power_off()
    print("Color test complete.")


def test_neopixel_fade():
    """Fade the LED in and out."""
    print("\n=== WS2812 Fade Test ===")
    power_on()

    led = WS2812(NEOPIXEL_DATA, NUM_LEDS, brightness=1.0)

    # Fade in (blue)
    for i in range(0, 256, 5):
        led.pixels_fill((0, 0, i))
        led.pixels_show()
        time.sleep_ms(20)

    # Fade out
    for i in range(255, -1, -5):
        led.pixels_fill((0, 0, i))
        led.pixels_show()
        time.sleep_ms(20)

    led.pixels_fill((0, 0, 0))
    led.pixels_show()
    power_off()
    print("Fade test complete.")


def test_neopixel_rainbow():
    """Rainbow color cycle."""
    print("\n=== WS2812 Rainbow Test ===")
    power_on()

    led = WS2812(NEOPIXEL_DATA, NUM_LEDS, brightness=1.0)
    led.rainbow_cycle(0.01)

    led.pixels_fill((0, 0, 0))
    led.pixels_show()
    power_off()
    print("Rainbow test complete.")


if __name__ == "__main__":
    print("XIAO RP2040 Plus - NeoPixel (WS2812) Test")
    print()
    test_neopixel_colors()
    test_neopixel_fade()
    test_neopixel_rainbow()
    print("\nNeoPixel test complete.")
