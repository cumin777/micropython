SEEED_XIAO_SAMD21_PLUS
======================

Board summary
-------------

- MCU: `SAMD21G18A`
- Default clock baseline: `48 MHz`
- Application offset: `0x2000`
- Default buses:
  - `UART(4)` on `D6`/`D7`
  - `I2C(2)` on `D4`/`D5`
  - `SPI(0)` on `D8`/`D9`/`D10`

Build
-----

Run these commands from the repository root:

```sh
make -C mpy-cross
make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS submodules
make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS clean
make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS
```

Expected artifacts:

- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.elf`
- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.bin`
- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.uf2`

UF2 notes
---------

The SAMD port generates UF2 directly via `tools/uf2conv.py`. For this board:

- UF2 family: `0x68ed2b88` from `ports/samd/mcu/samd21/mpconfigmcu.mk`
- UF2 base address: `0x2000` from `mpconfigboard.mk`

Flashing
--------

1. Double-tap reset to enter the bootloader.
2. Wait for the UF2 mass-storage drive to appear.
3. Copy `firmware.uf2` to the drive.
4. Wait for the drive to disappear and the board to reboot.

Serial validation
-----------------

Copy or paste `examples/hwapi/xiao_samd21_plus_serial_validation.py` to the
board and run it. Supported commands:

- `help`
- `id`
- `pinmap`
- `led`
- `txrxled`
- `gpio`
- `adc`
- `i2c-scan`
- `spi-loop` (`D10 -> D9` jumper required)
- `uart` (`D6 -> D7` jumper required)
- `pwm`
- `reset`
