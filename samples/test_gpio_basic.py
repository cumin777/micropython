# test_gpio_basic.py
# Test GPIO input/output for all new pins (D12-D17, D19-D27) on XIAO RP2040 Plus
# Hardware: Connect a LED + 330ohm resistor between each pin and GND for output test.
#           For input test, connect pin to GND (LOW) or 3V3 (HIGH) via a wire.

from machine import Pin
import time

# New pins on XIAO RP2040 Plus: {name: GPIO}
NEW_PINS = {
    "D12": 18, "D13": 19, "D14": 20, "D15": 21,
    "D16": 22, "D17": 23, "D19": 5, "D20": 13,
    "D21": 14, "D22": 15, "D23": 16, "D24": 17,
    "D25": 10, "D26": 9, "D27": 8,
}

def test_gpio_output():
    """Test all new pins as output - toggle HIGH/LOW."""
    print("=== GPIO Output Test ===")
    print("Each pin will toggle 3 times (1s interval).")
    for name, gpio in NEW_PINS.items():
        print(f"Testing {name} (GPIO{gpio}) as output...", end=" ")
        try:
            p = Pin(gpio, Pin.OUT)
            for i in range(3):
                p.value(1)
                time.sleep(0.5)
                p.value(0)
                time.sleep(0.5)
            print("OK")
        except Exception as e:
            print(f"FAIL: {e}")

def test_gpio_input():
    """Test all new pins as input with pull-up."""
    print("\n=== GPIO Input Test (with pull-up) ===")
    print("With pull-up enabled, unconnected pins should read HIGH (1).")
    print("Connect pin to GND to read LOW (0).")
    for name, gpio in NEW_PINS.items():
        try:
            p = Pin(gpio, Pin.IN, Pin.PULL_UP)
            val = p.value()
            status = "HIGH (floating/pulled up)" if val == 1 else "LOW (connected to GND)"
            print(f"  {name} (GPIO{gpio}): {val} - {status}")
        except Exception as e:
            print(f"  {name} (GPIO{gpio}): FAIL - {e}")

def test_gpio_input_pull_down():
    """Test all new pins as input with pull-down."""
    print("\n=== GPIO Input Test (with pull-down) ===")
    print("With pull-down enabled, unconnected pins should read LOW (0).")
    for name, gpio in NEW_PINS.items():
        try:
            p = Pin(gpio, Pin.IN, Pin.PULL_DOWN)
            val = p.value()
            status = "LOW (floating/pulled down)" if val == 0 else "HIGH (connected to 3V3)"
            print(f"  {name} (GPIO{gpio}): {val} - {status}")
        except Exception as e:
            print(f"  {name} (GPIO{gpio}): FAIL - {e}")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - GPIO Basic Test")
    print("Testing {} new pins".format(len(NEW_PINS)))
    print()
    test_gpio_output()
    test_gpio_input()
    test_gpio_input_pull_down()
    print("\nGPIO test complete.")
