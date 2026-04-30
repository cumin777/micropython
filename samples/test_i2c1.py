# test_i2c1.py
# Test I2C1 bus scan on XIAO RP2040 Plus (NEW feature on Plus board)
# I2C1: SDA=GPIO20, SCL=GPIO19
#
# NOTE: On RP2040, GPIO20 belongs to hardware I2C0 and GPIO19 belongs to
# hardware I2C1, so they cannot share a single hardware I2C instance.
# We use SoftI2C (bit-banged) which works on any GPIO pin.
#
# Hardware: Connect I2C devices to D14(SDA1)/D13(SCL1).
# For continuous scan, this script loops until interrupted (Ctrl+C).

from machine import Pin, SoftI2C
import time

# I2C1 configuration (new on XIAO RP2040 Plus)
I2C1_SDA = 20   # GPIO20 (D14/SDA1)
I2C1_SCL = 19   # GPIO19 (D13/SCL1)

def scan_once(i2c):
    """Perform a single scan and return device list."""
    devices = i2c.scan()
    return devices

def test_i2c1_scan():
    """Scan I2C1 bus once and report found devices."""
    print("=== I2C1 Bus Scan (NEW on Plus) ===")
    print("Using SoftI2C, SDA=GPIO{}, SCL=GPIO{}".format(I2C1_SDA, I2C1_SCL))
    print("  Connect I2C devices to D14(SDA1) / D13(SCL1)")

    try:
        i2c = SoftI2C(sda=Pin(I2C1_SDA), scl=Pin(I2C1_SCL), freq=400000)
        devices = scan_once(i2c)
        if devices:
            print("Found {} device(s):".format(len(devices)))
            for addr in devices:
                print("  - 0x{:02X} ({})".format(addr, addr))
        else:
            print("No I2C devices found on I2C1 bus.")
            print("  Check wiring: SDA to D14 (GPIO20), SCL to D13 (GPIO19)")
        return devices
    except Exception as e:
        print("I2C1 scan failed: {}".format(e))
        return []

def test_i2c1_continuous(interval=2):
    """Continuously scan I2C1 bus until Ctrl+C."""
    print("\n=== I2C1 Continuous Scan ===")
    print("Scanning every {}s. Press Ctrl+C to stop.".format(interval))

    try:
        i2c = SoftI2C(sda=Pin(I2C1_SDA), scl=Pin(I2C1_SCL), freq=400000)
    except Exception as e:
        print("Failed to init I2C1: {}".format(e))
        return

    count = 0
    try:
        while True:
            count += 1
            devices = scan_once(i2c)
            addrs = ["0x{:02X}".format(a) for a in devices]
            print("[{:>4d}] I2C1: {} device(s) {}".format(count, len(devices), addrs))
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nContinuous scan stopped after {} scans.".format(count))

def test_i2c_dual_bus():
    """Test both I2C buses simultaneously."""
    print("\n=== Dual I2C Bus Test ===")
    try:
        # I2C0: uses hardware I2C (GPIO6/GPIO7 belong to same i2c1 instance)
        i2c0 = SoftI2C(sda=Pin(6), scl=Pin(7), freq=400000)
        # I2C1: uses software I2C (GPIO20/GPIO19 span two hw instances)
        i2c1 = SoftI2C(sda=Pin(I2C1_SDA), scl=Pin(I2C1_SCL), freq=400000)
        dev0 = i2c0.scan()
        dev1 = i2c1.scan()
        print("I2C0 (SDA=GPIO6, SCL=GPIO7):  {} device(s) {}".format(
            len(dev0), ["0x{:02X}".format(a) for a in dev0]))
        print("I2C1 (SDA=GPIO20, SCL=GPIO19): {} device(s) {}".format(
            len(dev1), ["0x{:02X}".format(a) for a in dev1]))
    except Exception as e:
        print("Dual bus test failed: {}".format(e))

if __name__ == "__main__":
    print("XIAO RP2040 Plus - I2C1 Test (NEW)")
    print()
    test_i2c1_scan()
    test_i2c1_continuous()
    test_i2c_dual_bus()
    print("\nI2C1 test complete.")
