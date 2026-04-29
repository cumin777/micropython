# test_led.py
# Test user LED (GPIO25) on XIAO RP2040 Plus
# No external hardware needed - uses onboard LED.

from machine import Pin
import time

LED_PIN = 25  # GPIO25, active low

def test_led_blink(count=5, interval=0.5):
    """Blink the user LED specified number of times."""
    print(f"=== LED Blink Test ({count} times) ===")
    print(f"LED on GPIO{LED_PIN} (active low)")

    led = Pin(LED_PIN, Pin.OUT)

    for i in range(count):
        led.value(0)  # ON (active low)
        print(f"  LED ON")
        time.sleep(interval)
        led.value(1)  # OFF
        print(f"  LED OFF")
        time.sleep(interval)

    print("Blink test complete.")

def test_led_breathe(steps=20, cycles=3):
    """Simulate LED breathing effect using rapid toggling (no PWM)."""
    print(f"\n=== LED Rapid Toggle Test ({cycles} cycles) ===")
    led = Pin(LED_PIN, Pin.OUT)

    for cycle in range(cycles):
        for i in range(steps):
            # ON
            led.value(0)
            time.sleep_ms(5 + i * 2)
            # OFF
            led.value(1)
            time.sleep_ms(5 + (steps - i) * 2)
        for i in range(steps):
            # ON (fade in reverse)
            led.value(0)
            time.sleep_ms(5 + (steps - i) * 2)
            # OFF
            led.value(1)
            time.sleep_ms(5 + i * 2)

    led.value(1)  # Ensure LED is off
    print("Toggle test complete.")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - LED Test")
    print()
    test_led_blink()
    test_led_breathe()
    print("\nLED test complete.")
