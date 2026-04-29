# test_i2c0.py
# Test I2C0 bus scan on XIAO RP2040 Plus
# I2C0: SDA=GPIO6, SCL=GPIO7 (uses i2c1 hardware instance)
# Hardware: Connect I2C devices (sensors, displays, etc.) to D4(SDA)/D5(SCL).

from machine import I2C
import time

# I2C0 configuration
# Note: I2C0 uses hardware i2c1 (id=1), SDA=GPIO6, SCL=GPIO7
I2C0_ID = 0  # MicroPython I2C0 maps to hardware i2c1
I2C0_SDA = 6
I2C0_SCL = 7

def test_i2c0_scan():
    """Scan I2C0 bus and report found devices."""
    print("=== I2C0 Bus Scan ===")
    print(f"Using I2C(id={I2C0_ID}), SDA=GPIO{I2C0_SDA}, SCL=GPIO{I2C0_SCL}")

    try:
        i2c = I2C(I2C0_ID, sda=I2C0_SDA, scl=I2C0_SCL, freq=400000)
        devices = i2c.scan()
        if devices:
            print(f"Found {len(devices)} device(s):")
            for addr in devices:
                print(f"  - 0x{addr:02X} ({addr})")
        else:
            print("No I2C devices found.")
            print("Check wiring: SDA to D4 (GPIO6), SCL to D5 (GPIO7)")
        return devices
    except Exception as e:
        print(f"I2C0 scan failed: {e}")
        return []

if __name__ == "__main__":
    print("XIAO RP2040 Plus - I2C0 Test")
    print()
    test_i2c0_scan()
    print("\nI2C0 test complete.")
