# SAMD21 Plus Porting Progress

This file tracks verified milestones for the `SEEED_XIAO_SAMD21_PLUS` MicroPython port.

## Progress Entry Template
- Timestamp:
- Branch:
- Commit:
- Milestone:
- Files changed:
- Verification performed:
- Result:
- Blockers:
- Next action:

## Initial State
- Timestamp: 2026-05-11
- Branch: `xiao_samd21_plus_support`
- Commit: `23b8bbb1b417ba7baa1e092bcd6107bd0f2b10bc`
- Milestone: documentation bootstrap
- Files changed: `AGENT.md`, `SAMD21_PLUS_PORTING_PROGRESS.md`
- Verification performed: inspected `ports/samd/boards/SEEED_XIAO_SAMD21`, `variant.h`, and `variant.cpp` from ArduinoCore source of truth
- Result: requirements understood before implementation migrated into the live git checkout
- Blockers: none at this stage
- Next action: implement milestone 1 in the live `cumin777/micropython` checkout

## 2026-05-11 16:20 Milestone 1
- Timestamp: 2026-05-11 16:20 +08:00
- Branch: `xiao_samd21_plus_support`
- Commit: `23b8bbb1b417ba7baa1e092bcd6107bd0f2b10bc`
- Milestone: board skeleton and pin map
- Files changed: `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS/board.json`, `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS/mpconfigboard.h`, `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS/mpconfigboard.mk`, `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS/pins.csv`
- Verification performed: compared against `ports/samd/boards/SEEED_XIAO_SAMD21/*`; checked ArduinoCore source of truth in `D:\workspace\seeedunio\ArduinoCore-samd\variants\XIAO_m0_plus\variant.h` and `variant.cpp`; confirmed default UART/I2C/SPI IDs remain supported by `ports/samd/mpconfigport.h`
- Result: new board skeleton added with required `D0..D10`, `A0..A10`, `LED`, `TX_LED`, `RX_LED`, `SDA`, `SCL`, `TX`, `RX`, `SCK`, `MISO`, and `MOSI` aliases; USB/SWD pins intentionally not exposed
- Blockers: host environment does not yet provide the full SAMD build toolchain
- Next action: run board-targeted build verification and confirm UF2 artifact path

## 2026-05-11 16:34 Milestone 3 Prep
- Timestamp: 2026-05-11 16:34 +08:00
- Branch: `xiao_samd21_plus_support`
- Commit: `e050aac7cbd35a6b2805ff15c9fc9a08caecf4d4`
- Milestone: UF2 generation path and serial validation assets
- Files changed: `examples/hwapi/xiao_samd21_plus_serial_validation.py`, `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS/README.md`, `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS/pins.csv`
- Verification performed: `python -m py_compile examples/hwapi/xiao_samd21_plus_serial_validation.py`; generated board pin sources with `python boards/make-pins.py --board-csv boards/SEEED_XIAO_SAMD21_PLUS/pins.csv --af-csv mcu/samd21/pin-af-table.csv --prefix boards/pins_prefix.c --output-source build-test/pins_SEEED_XIAO_SAMD21_PLUS.c --output-header build-test/pins.h --mcu SAMD21`; inspected `ports/samd/Makefile`, `ports/samd/mcu/samd21/mpconfigmcu.mk`, and `ports/samd/boards/deploy.md`
- Result: serial validation sample added; documented direct UF2 path at `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.uf2`; confirmed UF2 metadata should use family `0x68ed2b88` and base address `0x2000`
- Blockers: host environment is missing `make` and `arm-none-eabi-gcc`, so firmware build and UF2 artifact generation could not be executed locally
- Next action: install build prerequisites, then run `make -C mpy-cross` and `make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS`

## 2026-05-11 17:05 Final Validation
- Timestamp: 2026-05-11 17:05 +08:00
- Branch: `xiao_samd21_plus_support`
- Commit: pending final docs commit
- Milestone: final validation and documentation cleanup
- Files changed: `SAMD21_PLUS_PORTING_PROGRESS.md`
- Verification performed: `wsl.exe -e sh -lc "cd /mnt/d/workspace/micropython-git && make -C mpy-cross"`; `wsl.exe -e sh -lc "cd /mnt/d/workspace/micropython-git && make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS submodules"`; `wsl.exe -e sh -lc "cd /mnt/d/workspace/micropython-git && make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS clean && make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS -j1"`; confirmed `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.uf2` exists at 374272 bytes; checked `arm-none-eabi-size ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.elf`
- Result: clean rebuild succeeded; UF2 artifact generated directly by the SAMD port; serial validation sample remains syntax-valid and build target is selectable
- Blockers: hardware flashing and on-device serial test execution remain unverified in this environment
- Next action: push branch and, on hardware, flash the UF2 and run `examples/hwapi/xiao_samd21_plus_serial_validation.py`

## 2026-05-15 00:00 AGENT Sync
- Timestamp: 2026-05-15 +08:00
- Branch: `xiao_samd21_plus_support`
- Commit: pending AGENT sync commit
- Milestone: root AGENT guide sync into live git branch
- Files changed: `AGENT.md`, `SAMD21_PLUS_PORTING_PROGRESS.md`
- Verification performed: reviewed the live branch history; confirmed `AGENT.md` was missing while prior implementation and milestone log entries already existed; synced the root execution guide without altering existing board, UF2, or sample code
- Result: repository root now contains the execution guide required for the documented workflow
- Blockers: none for this documentation sync; hardware flashing and on-device serial validation remain outside this environment
- Next action: commit and push the AGENT guide to origin
