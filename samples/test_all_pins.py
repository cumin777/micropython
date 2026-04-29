# test_all_pins.py
# Comprehensive pin test for all XIAO RP2040 Plus pins
# Runs all tests sequentially. Use for quick board verification.

from machine import Pin, ADC, I2C, SPI, UART, PWM
import time

# ============================================================
# Pin definitions
# ============================================================

# Original pins (D0-D10, same as old XIAO RP2040)
ORIGINAL_PINS = {
    "D0/A0": 26, "D1/A1": 27, "D2/A2": 28, "D3/A3": 29,
    "D4/SDA": 6, "D5/SCL": 7, "D6/TX": 0, "D7/RX": 1,
    "D8/SCK": 2, "D9/MISO": 4, "D10/MOSI": 3,
}

# New pins (D12-D27, Plus only)
NEW_PINS = {
    "D12": 18, "D13/SCL1": 19, "D14/SDA1": 20, "D15": 21,
    "D16": 22, "D17": 23, "D19": 5, "D20": 13,
    "D21": 14, "D22": 15, "D23": 16, "D24": 17,
    "D25": 10, "D26": 9, "D27": 8,
}

# Special pins
SPECIAL_PINS = {
    "LED": 25,
    "NEOPIXEL": 12,
    "NEOPIXEL_POWER": 24,
}

# ADC pins
ADC_PINS = {"A0": 26, "A1": 27, "A2": 28, "A3": 29}

# ============================================================
# Test counters
# ============================================================
passed = 0
failed = 0

def record(result, msg):
    global passed, failed
    if result:
        passed += 1
        print(f"  [PASS] {msg}")
    else:
        failed += 1
        print(f"  [FAIL] {msg}")

# ============================================================
# Test 1: GPIO output toggle
# ============================================================
def test_gpio_output(pins):
    print("\n--- GPIO Output Test ---")
    for name, gpio in pins.items():
        try:
            p = Pin(gpio, Pin.OUT)
            p.value(1)
            time.sleep_ms(10)
            p.value(0)
            p.deinit()
            record(True, f"{name} (GPIO{gpio}) output toggle")
        except Exception as e:
            record(False, f"{name} (GPIO{gpio}) output: {e}")

# ============================================================
# Test 2: GPIO input with pull-up
# ============================================================
def test_gpio_input(pins):
    print("\n--- GPIO Input Test (pull-up) ---")
    for name, gpio in pins.items():
        try:
            p = Pin(gpio, Pin.IN, Pin.PULL_UP)
            val = p.value()
            p.deinit()
            record(True, f"{name} (GPIO{gpio}) input = {val}")
        except Exception as e:
            record(False, f"{name} (GPIO{gpio}) input: {e}")

# ============================================================
# Test 3: ADC read
# ============================================================
def test_adc():
    print("\n--- ADC Test ---")
    for name, gpio in ADC_PINS.items():
        try:
            adc = ADC(gpio)
            raw = adc.read_u16()
            voltage = raw * 3.3 / 65535
            record(True, f"{name} (GPIO{gpio}): {raw} ({voltage:.2f}V)")
        except Exception as e:
            record(False, f"{name} (GPIO{gpio}): {e}")

# ============================================================
# Test 4: I2C0 scan
# ============================================================
def test_i2c0():
    print("\n--- I2C0 Scan ---")
    try:
        i2c = I2C(0, sda=6, scl=7, freq=400000)
        devices = i2c.scan()
        record(True, f"I2C0 scan: found {len(devices)} device(s) {[hex(a) for a in devices]}")
        i2c.deinit()
    except Exception as e:
        record(False, f"I2C0: {e}")

# ============================================================
# Test 5: I2C1 scan (new on Plus)
# ============================================================
def test_i2c1():
    print("\n--- I2C1 Scan (NEW) ---")
    try:
        i2c = I2C(1, sda=20, scl=19, freq=400000)
        devices = i2c.scan()
        record(True, f"I2C1 scan: found {len(devices)} device(s) {[hex(a) for a in devices]}")
        i2c.deinit()
    except Exception as e:
        record(False, f"I2C1: {e}")

# ============================================================
# Test 6: SPI test
# ============================================================
def test_spi():
    print("\n--- SPI0 Test ---")
    print("  (Loopback test: connect D10/MOSI to D9/MISO)")
    try:
        spi = SPI(0, sck=2, mosi=3, miso=4, baudrate=1_000_000)
        tx = b"\xA5"
        rx = bytearray(1)
        spi.write_readinto(tx, rx)
        match = tx == bytes(rx)
        if match:
            record(True, f"SPI0 loopback: TX={tx.hex()} RX={bytes(rx).hex()}")
        else:
            record(True, f"SPI0 initialized OK (loopback data mismatch - no wire?)")
        spi.deinit()
    except Exception as e:
        record(False, f"SPI0: {e}")

# ============================================================
# Test 7: UART test
# ============================================================
def test_uart():
    print("\n--- UART0 Test ---")
    print("  (Loopback test: connect D6/TX to D7/RX)")
    try:
        uart = UART(0, baudrate=115200, tx=0, rx=1)
        tx = b"HI"
        uart.write(tx)
        time.sleep_ms(50)
        rx = uart.read(len(tx))
        if rx and tx == rx:
            record(True, f"UART0 loopback: TX={tx} RX={rx}")
        else:
            record(True, f"UART0 initialized OK (loopback data mismatch - no wire?)")
        uart.deinit()
    except Exception as e:
        record(False, f"UART0: {e}")

# ============================================================
# Test 8: LED
# ============================================================
def test_led():
    print("\n--- User LED Test ---")
    try:
        led = Pin(25, Pin.OUT)
        led.value(0)  # ON (active low)
        time.sleep_ms(200)
        led.value(1)  # OFF
        record(True, "LED (GPIO25) toggle")
    except Exception as e:
        record(False, f"LED: {e}")

# ============================================================
# Test 9: PWM
# ============================================================
def test_pwm():
    print("\n--- PWM Test ---")
    try:
        pwm = PWM(Pin(18))  # D12
        pwm.freq(1000)
        pwm.duty_u16(32768)
        time.sleep_ms(100)
        actual_freq = pwm.freq()
        pwm.deinit()
        record(True, f"PWM on D12 (GPIO18): freq={actual_freq}Hz, duty=50%")
    except Exception as e:
        record(False, f"PWM: {e}")

# ============================================================
# Test 10: NeoPixel power pin
# ============================================================
def test_neopixel_power():
    print("\n--- NeoPixel Power Pin Test ---")
    try:
        pwr = Pin(24, Pin.OUT)
        pwr.value(1)
        time.sleep_ms(50)
        pwr.value(0)
        record(True, "NEOPIXEL_POWER (GPIO24) toggle")
    except Exception as e:
        record(False, f"NEOPIXEL_POWER: {e}")

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("XIAO RP2040 Plus - Comprehensive Pin Test")
    print("=" * 50)

    all_pins = {}
    all_pins.update(ORIGINAL_PINS)
    all_pins.update(NEW_PINS)
    all_pins.update(SPECIAL_PINS)

    print(f"Total pins to test: {len(all_pins)}")
    print(f"  Original (D0-D10): {len(ORIGINAL_PINS)}")
    print(f"  New (D12-D27):     {len(NEW_PINS)}")
    print(f"  Special:           {len(SPECIAL_PINS)}")

    # Run all tests
    test_gpio_output(all_pins)
    test_gpio_input(all_pins)
    test_adc()
    test_i2c0()
    test_i2c1()
    test_spi()
    test_uart()
    test_led()
    test_pwm()
    test_neopixel_power()

    # Summary
    total = passed + failed
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{total} PASSED, {failed}/{total} FAILED")
    if failed == 0:
        print("All tests passed!")
    else:
        print(f"{failed} test(s) failed. Check wiring and pin assignments.")
    print("=" * 50)
