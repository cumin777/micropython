# test_adc.py
# Test ADC analog input (A0-A3 / GPIO26-29) on XIAO RP2040 Plus
# Hardware: Connect potentiometer or voltage divider to each ADC pin.

from machine import ADC, Pin
import time

# ADC pins (shared with D0-D3)
ADC_PINS = {
    "A0": 26,  # GPIO26 / D0
    "A1": 27,  # GPIO27 / D1
    "A2": 28,  # GPIO28 / D2
    "A3": 29,  # GPIO29 / D3
}

def test_adc_read():
    """Read all ADC pins once."""
    print("=== ADC Single Read Test ===")
    for name, gpio in ADC_PINS.items():
        try:
            adc = ADC(gpio)
            raw = adc.read_u16()
            voltage = raw * 3.3 / 65535
            print(f"  {name} (GPIO{gpio}): raw={raw:5d}, voltage={voltage:.3f}V")
        except Exception as e:
            print(f"  {name} (GPIO{gpio}): FAIL - {e}")

def test_adc_continuous(duration=5):
    """Continuously read all ADC pins for specified duration (seconds)."""
    print(f"\n=== ADC Continuous Read ({duration}s) ===")
    print("Readings every 0.5s. Press Ctrl+C to stop early.")
    adcs = {}
    for name, gpio in ADC_PINS.items():
        adcs[name] = ADC(gpio)

    start = time.time()
    try:
        while time.time() - start < duration:
            readings = []
            for name, adc in adcs.items():
                raw = adc.read_u16()
                voltage = raw * 3.3 / 65535
                readings.append(f"{name}={voltage:.2f}V")
            print("  " + " | ".join(readings))
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n  Stopped by user.")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - ADC Test")
    print("Testing {} ADC pins".format(len(ADC_PINS)))
    print()
    test_adc_read()
    test_adc_continuous(duration=5)
    print("\nADC test complete.")
