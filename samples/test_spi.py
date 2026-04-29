# test_spi.py
# Test SPI0 loopback on XIAO RP2040 Plus
# SPI0: SCK=GPIO2, MOSI=GPIO3, MISO=GPIO4
# Hardware: Connect MOSI (D10/GPIO3) to MISO (D9/GPIO4) for loopback test.

from machine import SPI
import time

# SPI0 configuration
SPI_ID = 0
SPI_SCK = 2   # GPIO2 / D8
SPI_MOSI = 3  # GPIO3 / D10
SPI_MISO = 4  # GPIO4 / D9

def test_spi_loopback():
    """Test SPI by sending data and reading it back via loopback."""
    print("=== SPI0 Loopback Test ===")
    print(f"SPI(id={SPI_ID}), SCK=GPIO{SPI_SCK}, MOSI=GPIO{SPI_MOSI}, MISO=GPIO{SPI_MISO}")
    print("Connect MOSI (D10/GPIO3) to MISO (D9/GPIO4) for loopback.")

    try:
        spi = SPI(SPI_ID, sck=SPI_SCK, mosi=SPI_MOSI, miso=SPI_MISO, baudrate=1_000_000)

        # Test with different data patterns
        test_patterns = [
            (b"\x55\xAA", "0x55/0xAA toggle"),
            (b"\x00\xFF", "0x00/0xFF edge"),
            (b"\x0F\xF0", "0x0F/0xF0 nibble"),
            (b"\x12\x34\x56\x78", "sequential"),
        ]

        all_passed = True
        for tx_data, desc in test_patterns:
            rx_data = bytearray(len(tx_data))
            spi.write_readinto(tx_data, rx_data)
            match = tx_data == bytes(rx_data)
            status = "PASS" if match else "FAIL"
            if not match:
                all_passed = False
            print(f"  {desc}: TX={tx_data.hex()} RX={bytes(rx_data).hex()} [{status}]")

        if all_passed:
            print("\nAll loopback tests passed!")
        else:
            print("\nSome tests failed. Ensure MOSI-MISO loopback wire is connected.")

        spi.deinit()
        return all_passed

    except Exception as e:
        print(f"SPI test failed: {e}")
        return False

def test_spi_baudrate():
    """Test SPI at different baud rates."""
    print("\n=== SPI Baud Rate Test ===")
    baudrates = [500_000, 1_000_000, 5_000_000, 10_000_000]
    test_data = b"\xA5\x5A"

    for baud in baudrates:
        try:
            spi = SPI(SPI_ID, sck=SPI_SCK, mosi=SPI_MOSI, miso=SPI_MISO, baudrate=baud)
            rx = bytearray(len(test_data))
            spi.write_readinto(test_data, rx)
            match = test_data == bytes(rx)
            print(f"  {baud/1e6:.1f} MHz: {'PASS' if match else 'FAIL'}")
            spi.deinit()
        except Exception as e:
            print(f"  {baud/1e6:.1f} MHz: FAIL - {e}")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - SPI Test")
    print()
    test_spi_loopback()
    test_spi_baudrate()
    print("\nSPI test complete.")
