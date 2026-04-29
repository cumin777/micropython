# test_uart.py
# Test UART0 loopback on XIAO RP2040 Plus
# UART0: TX=GPIO0, RX=GPIO1
# Hardware: Connect TX (D6/GPIO0) to RX (D7/GPIO1) for loopback test.

from machine import UART
import time

# UART0 configuration
UART_ID = 0
UART_TX = 0  # GPIO0 / D6
UART_RX = 1  # GPIO1 / D7

def test_uart_loopback():
    """Test UART by sending data and reading it back via loopback."""
    print("=== UART0 Loopback Test ===")
    print(f"UART(id={UART_ID}), TX=GPIO{UART_TX}, RX=GPIO{UART_RX}")
    print("Connect TX (D6/GPIO0) to RX (D7/GPIO1) for loopback.")

    try:
        uart = UART(UART_ID, baudrate=115200, tx=UART_TX, rx=UART_RX)

        # Test patterns
        test_patterns = [
            (b"Hello XIAO RP2040 Plus!\r\n", "text message"),
            (b"\x00\xFF\x55\xAA", "binary data"),
            (b"0123456789", "numeric string"),
        ]

        all_passed = True
        for tx_data, desc in test_patterns:
            uart.write(tx_data)
            time.sleep_ms(50)  # Wait for data to arrive
            rx_data = uart.read(len(tx_data))
            if rx_data is None:
                print(f"  {desc}: FAIL - no data received")
                all_passed = False
                continue
            match = tx_data == rx_data
            status = "PASS" if match else "FAIL"
            if not match:
                all_passed = False
            print(f"  {desc}: TX={len(tx_data)}B RX={len(rx_data)}B [{status}]")

        if all_passed:
            print("\nAll loopback tests passed!")
        else:
            print("\nSome tests failed. Ensure TX-RX loopback wire is connected.")

        uart.deinit()
        return all_passed

    except Exception as e:
        print(f"UART test failed: {e}")
        return False

def test_uart_baudrates():
    """Test UART at different baud rates."""
    print("\n=== UART Baud Rate Test ===")
    baudrates = [9600, 19200, 38400, 57600, 115200]
    test_msg = b"TEST"

    for baud in baudrates:
        try:
            uart = UART(UART_ID, baudrate=baud, tx=UART_TX, rx=UART_RX)
            uart.write(test_msg)
            time.sleep_ms(100)
            rx = uart.read(len(test_msg))
            match = test_msg == rx if rx else False
            print(f"  {baud:>6d} baud: {'PASS' if match else 'FAIL'}")
            uart.deinit()
        except Exception as e:
            print(f"  {baud:>6d} baud: FAIL - {e}")

if __name__ == "__main__":
    print("XIAO RP2040 Plus - UART Test")
    print()
    test_uart_loopback()
    test_uart_baudrates()
    print("\nUART test complete.")
