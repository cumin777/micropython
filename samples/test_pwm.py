# test_pwm.py
# Test PWM output on XIAO RP2040 Plus
# Hardware: Connect LED + 330ohm resistor to test pin for visible dimming.

from machine import PWM, Pin
import time

# Test pins (select from new pins)
TEST_PINS = [
    ("D12", 18),
    ("D19", 5),
    ("D20", 13),
]

def test_pwm_basic():
    """Test basic PWM output with different duty cycles."""
    print("=== PWM Basic Test ===")
    for name, gpio in TEST_PINS:
        print(f"\nTesting {name} (GPIO{gpio}):")
        try:
            pwm = PWM(Pin(gpio))
            pwm.freq(1000)  # 1kHz

            # Test duty cycle sweep: 0% -> 100% -> 0%
            print("  Sweeping duty cycle 0-100%...")
            for duty in range(0, 65536, 2560):
                pwm.duty_u16(duty)
                time.sleep_ms(20)

            print("  Sweeping duty cycle 100-0%...")
            for duty in range(65535, -1, -2560):
                pwm.duty_u16(duty)
                time.sleep_ms(20)

            pwm.duty_u16(0)
            pwm.deinit()
            print(f"  {name} PWM OK")
        except Exception as e:
            print(f"  {name} PWM FAIL: {e}")

def test_pwm_freq_sweep():
    """Test PWM at different frequencies."""
    print("\n=== PWM Frequency Sweep Test ===")
    name, gpio = TEST_PINS[0]
    print(f"Using {name} (GPIO{gpio})")

    try:
        pwm = PWM(Pin(gpio))
        freqs = [100, 500, 1000, 5000, 10000, 50000, 100000]

        for freq in freqs:
            pwm.freq(freq)
            pwm.duty_u16(32768)  # 50% duty cycle
            actual_freq = pwm.freq()
            print(f"  Requested: {freq:>7d} Hz, Actual: {actual_freq:>7d} Hz")
            time.sleep_ms(500)

        pwm.deinit()
        print("Frequency sweep complete.")
    except Exception as e:
        print(f"Frequency sweep failed: {e}")

def test_pwm_breathing_led():
    """Simulate breathing LED effect using PWM."""
    print("\n=== PWM Breathing LED Test ===")
    name, gpio = TEST_PINS[0]
    print(f"Using {name} (GPIO{gpio}), 3 cycles")

    try:
        pwm = PWM(Pin(gpio))
        pwm.freq(1000)

        for cycle in range(3):
            print(f"  Cycle {cycle + 1}...")
            # Fade in
            for duty in range(0, 65536, 256):
                pwm.duty_u16(duty)
                time.sleep_ms(10)
            # Fade out
            for duty in range(65535, -1, -256):
                pwm.duty_u16(duty)
                time.sleep_ms(10)

        pwm.deinit()
        print("Breathing LED test complete.")
    except Exception as e:
        print(f"Breathing LED test failed: {e}")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - PWM Test")
    print()
    test_pwm_basic()
    test_pwm_freq_sweep()
    test_pwm_breathing_led()
    print("\nPWM test complete.")
