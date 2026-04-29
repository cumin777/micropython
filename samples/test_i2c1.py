# test_i2c1.py
# Test I2C1 bus scan on XIAO RP2040 Plus (NEW feature on Plus board)
# I2C1: SDA=GPIO20, SCL=GPIO19 (uses i2c0 hardware instance)
# Hardware: Connect I2C devices to D14(SDA1)/D13(SCL1).

from machine import I2C
import time

# I2C1 configuration (new on XIAO RP2040 Plus)
# Note: I2C1 uses hardware i2c0 (id=0), SDA=GPIO20, SCL=GPIO19
I2C1_ID = 1  # MicroPython I2C1 maps to hardware i2c0
I2C1_SDA = 20
I2C1_SCL = 19

def test_i2c1_scan():
    """Scan I2C1 bus and report found devices."""
    print("=== I2C1 Bus Scan (NEW on Plus) ===")
    print(f"Using I2C(id={I2C1_ID}), SDA=GPIO{I2C1_SDA}, SCL=GPIO{I2C1_SCL}")

    try:
        i2c = I2C(I2C1_ID, sda=I2C1_SDA, scl=I2C1_SCL, freq=400000)
        devices = i2c.scan()
        if devices:
            print(f"Found {len(devices)} device(s):")
            for addr in devices:
                print(f"  - 0x{addr:02X} ({addr})")
        else:
            print("No I2C devices found.")
            print("Check wiring: SDA to D14 (GPIO20), SCL to D13 (GPIO19)")
        return devices
    except Exception as e:
        print(f"I2C1 scan failed: {e}")
        return []

def test_i2c_dual_bus():
    """Test both I2C buses simultaneously."""
    print("\n=== Dual I2C Bus Test ===")
    try:
        i2c0 = I2C(0, sda=6, scl=7, freq=400000)
        i2c1 = I2C(1, sda=20, scl=19, freq=400000)
        dev0 = i2c0.scan()
        dev1 = i2c1.scan()
        print(f"I2C0 devices: {[hex(a) for a in dev0]}")
        print(f"I2C1 devices: {[hex(a) for a in dev1]}")
    except Exception as e:
        print(f"Dual bus test failed: {e}")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - I2C1 Test (NEW)")
    print()
    test_i2c1_scan()
    test_i2c_dual_bus()
    print("\nI2C1 test complete.")
