import os
import sys
import time
import machine
import micropython
from machine import ADC, I2C, PWM, SPI, UART, Pin


BOARD_NAME = "SEEED_XIAO_SAMD21_PLUS"
FW_INFO = "{} on {}".format(sys.implementation.name, os.uname().machine)

PINMAP = {
    "LED": "LED",
    "TX_LED": "TX_LED",
    "RX_LED": "RX_LED",
    "D0": "D0",
    "D1": "D1",
    "D2": "D2",
    "D3": "D3",
    "D4_SDA": "D4",
    "D5_SCL": "D5",
    "D6_TX": "D6",
    "D7_RX": "D7",
    "D8_SCK": "D8",
    "D9_MISO": "D9",
    "D10_MOSI": "D10",
    "D11_TX_LED": "D11",
    "D12_RX_LED": "D12",
    "D13_LED": "D13",
    "A0": "A0",
    "A1": "A1",
    "A2": "A2",
    "A3": "A3",
    "A4": "A4",
    "A5": "A5",
    "A6": "A6",
    "A7": "A7",
    "A8": "A8",
    "A9": "A9",
    "A10": "A10",
}

ADC_PINS = ("A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10")
SAFE_OUTPUT_PINS = ("D0", "D1", "D2", "D3")
resources = []


def track(obj):
    resources.append(obj)
    return obj


def cleanup():
    while resources:
        obj = resources.pop()
        try:
            obj.deinit()
            continue
        except AttributeError:
            pass
        except Exception:
            pass
        try:
            obj.init(Pin.IN)
        except Exception:
            pass
    for pin_name in SAFE_OUTPUT_PINS + ("LED", "TX_LED", "RX_LED"):
        try:
            Pin(pin_name, Pin.IN)
        except Exception:
            pass


def report(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    if detail:
        print("{}: {} - {}".format(name, status, detail))
    else:
        print("{}: {}".format(name, status))


def cmd_help():
    print("Commands:")
    print("  help      show this menu")
    print("  id        print board and firmware information")
    print("  pinmap    print logical pin map")
    print("  led       blink built-in LED on D13/LED")
    print("  txrxled   toggle D11/TX_LED and D12/RX_LED")
    print("  gpio      test safe GPIO on D0..D3")
    print("  adc       read A0..A10")
    print("  i2c-scan  scan I2C on D4/D5")
    print("  spi-loop  requires D10->D9 jumper; clock on D8")
    print("  uart      requires D6->D7 jumper")
    print("  pwm       drive PWM on D1")
    print("  reset     restore pins and return to idle")


def cmd_id():
    print("Board: {}".format(BOARD_NAME))
    print("Firmware: {}".format(FW_INFO))
    print("Version: {}".format(sys.version))
    print("Freq: {}".format(machine.freq()))
    report("id", True)


def cmd_pinmap():
    for key in sorted(PINMAP):
        print("{:8s} {}".format(key, PINMAP[key]))
    report("pinmap", True)


def cmd_led():
    led = track(Pin("LED", Pin.OUT, value=0))
    for _ in range(3):
        led.value(1)
        time.sleep_ms(150)
        led.value(0)
        time.sleep_ms(150)
    report("led", True, "blinked LED")


def cmd_txrxled():
    tx_led = track(Pin("TX_LED", Pin.OUT, value=0))
    rx_led = track(Pin("RX_LED", Pin.OUT, value=0))
    for _ in range(3):
        tx_led.value(1)
        rx_led.value(1)
        time.sleep_ms(120)
        tx_led.value(0)
        rx_led.value(0)
        time.sleep_ms(120)
    report("txrxled", True, "toggled TX/RX LEDs")


def cmd_gpio():
    observed = []
    for name in SAFE_OUTPUT_PINS:
        out_pin = track(Pin(name, Pin.OUT, value=0))
        out_pin.value(1)
        time.sleep_ms(5)
        observed.append((name, out_pin.value()))
        out_pin.value(0)
    ok = all(v == 1 for _, v in observed)
    report("gpio", ok, str(observed))


def cmd_adc():
    for name in ADC_PINS:
        adc = track(ADC(Pin(name)))
        print("{}={}".format(name, adc.read_u16()))
    report("adc", True)


def cmd_i2c_scan():
    i2c = track(I2C(2, scl=Pin("D5"), sda=Pin("D4"), freq=100000))
    devices = i2c.scan()
    report("i2c-scan", True, "devices={}".format(devices))


def cmd_spi_loop():
    spi = track(SPI(0, baudrate=500000, polarity=0, phase=0, sck=Pin("D8"), mosi=Pin("D10"), miso=Pin("D9")))
    tx = b"SPI"
    rx = bytearray(len(tx))
    spi.write_readinto(tx, rx)
    ok = bytes(rx) == tx
    detail = "received={!r}; jumper D10->D9 required".format(bytes(rx))
    report("spi-loop", ok, detail)


def _uart_read(uart, timeout_ms):
    start = time.ticks_ms()
    data = b""
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        if uart.any():
            chunk = uart.read()
            if chunk:
                data += chunk
                break
        time.sleep_ms(10)
    return data


def cmd_uart():
    uart = track(UART(4, baudrate=115200, tx=Pin("D6"), rx=Pin("D7")))
    tx = b"UART\r\n"
    uart.write(tx)
    rx = _uart_read(uart, 400)
    ok = rx == tx
    detail = "received={!r}; jumper D6->D7 required".format(rx)
    report("uart", ok, detail)


def cmd_pwm():
    pwm = track(PWM(Pin("D1"), freq=1000, duty_u16=32768))
    time.sleep_ms(250)
    report("pwm", True, "D1 duty=32768 freq=1000")


def cmd_reset():
    cleanup()
    report("reset", True)


COMMANDS = {
    "help": cmd_help,
    "id": cmd_id,
    "pinmap": cmd_pinmap,
    "led": cmd_led,
    "txrxled": cmd_txrxled,
    "gpio": cmd_gpio,
    "adc": cmd_adc,
    "i2c-scan": cmd_i2c_scan,
    "spi-loop": cmd_spi_loop,
    "uart": cmd_uart,
    "pwm": cmd_pwm,
    "reset": cmd_reset,
}


def run_command(line):
    func = COMMANDS.get(line)
    if func is None:
        report(line, False, "unknown command")
        return
    try:
        func()
    except Exception as exc:
        report(line, False, "{}: {}".format(type(exc).__name__, exc))
    finally:
        cleanup()
        print("idle")


def main():
    micropython.alloc_emergency_exception_buf(100)
    print("{} serial validation".format(BOARD_NAME))
    cmd_help()
    print("idle")
    while True:
        try:
            line = input("cmd> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            cmd_reset()
            continue
        if not line:
            continue
        run_command(line)


main()
