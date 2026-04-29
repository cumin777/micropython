# test_neopixel.py
# Test WS2812B RGB LED (GPIO12) with power control (GPIO24) on XIAO RP2040 Plus
# No external hardware needed - uses onboard RGB LED.

from machine import Pin
import time

# Use the NeoPixel driver from rp2 PIO
try:
    from rp2 import PIO, StateMachine
except ImportError:
    print("This test requires rp2 PIO support.")

# WS2812 pins
NEOPIXEL_DATA = 12    # GPIO12
NEOPIXEL_POWER = 24   # GPIO24 (active high)

# WS2812 timing parameters
T1 = 2  # High time for '1' bit (cycles @ 125MHz, ~800ns)
T2 = 5  # Low time for '1' bit
T3 = 3  # High time for '0' bit
T4 = 4  # Low time for '0' bit

@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24,
)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    T4 = 4
    wrap_target()
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, bit_zero)    .side(1)    [T1 - 1]
    jmp(bit_one)            .side(1)    [T2 - 1]
    bit_zero:
    nop()                   .side(0)    [T4 - 1]
    bit_one:
    wrap()

def power_on():
    """Enable WS2812 power."""
    pwr = Pin(NEOPIXEL_POWER, Pin.OUT)
    pwr.value(1)
    time.sleep_ms(10)

def power_off():
    """Disable WS2812 power."""
    pwr = Pin(NEOPIXEL_POWER, Pin.OUT)
    pwr.value(0)

def set_color(sm, r, g, b):
    """Set WS2812 color. Data format: G R B (24 bits)."""
    data = (g << 16) | (r << 8) | b
    sm.put(data, 0)

def test_neopixel_colors():
    """Cycle through basic colors."""
    print("=== WS2812 RGB LED Color Test ===")
    print(f"Data=GPIO{NEOPIXEL_DATA}, Power=GPIO{NEOPIXEL_POWER}")

    power_on()

    # Create state machine
    sm = StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(NEOPIXEL_DATA))
    sm.active(1)

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
        set_color(sm, r, g, b)
        print(f"  Color: {name} (R={r}, G={g}, B={b})")
        time.sleep(1)

    sm.active(0)
    power_off()
    print("Color test complete.")

def test_neopixel_fade():
    """Fade the LED in and out."""
    print("\n=== WS2812 Fade Test ===")
    power_on()

    sm = StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(NEOPIXEL_DATA))
    sm.active(1)

    # Fade in
    for i in range(0, 256, 5):
        set_color(sm, 0, 0, i)
        time.sleep_ms(20)

    # Fade out
    for i in range(255, -1, -5):
        set_color(sm, 0, 0, i)
        time.sleep_ms(20)

    set_color(sm, 0, 0, 0)
    sm.active(0)
    power_off()
    print("Fade test complete.")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - NeoPixel (WS2812) Test")
    print()
    test_neopixel_colors()
    test_neopixel_fade()
    print("\nNeoPixel test complete.")
