# XIAO SAMD21 Plus MicroPython Porting Agent Guide

## Mission
Port `samd21 plus` to `cumin777/micropython` as a new independent board named `SEEED_XIAO_SAMD21_PLUS`.

This guide defines the required workflow, deliverables, validation gates, commit sequence, and progress tracking rules for the full porting effort.

## Non-Negotiable Workflow
- Start from the upstream default branch, then create a new branch named `xiao_samd21_plus_support`.
- Never develop on the default branch.
- Before each change, inspect the closest existing implementation first.
- Change only one logical slice at a time.
- Run the narrowest useful verification immediately after each slice.
- Commit and push only after that slice passes verification.
- After each verified slice, append a progress entry to `SAMD21_PLUS_PORTING_PROGRESS.md`.

Treat `superpower mcp` as a process discipline:
- inspect before editing
- prefer the smallest viable change
- verify early
- keep milestones independently reviewable
- log every verified step

## Required Deliverables
- A new MicroPython board definition under `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS`
- A documented and reproducible UF2 firmware build path for the board
- A serial-command-driven MicroPython validation sample for the board
- A root progress log named `SAMD21_PLUS_PORTING_PROGRESS.md`

## Source Of Truth
Board pin and interface mapping must be derived from:
- `D:\workspace\seeedunio\ArduinoCore-samd\variants\XIAO_m0_plus\variant.h`
- `D:\workspace\seeedunio\ArduinoCore-samd\variants\XIAO_m0_plus\variant.cpp`

Use the existing MicroPython board below as the primary template:
- `ports/samd/boards/SEEED_XIAO_SAMD21`

## Board Identity
- Board directory: `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS`
- Board name macro: `SEEED_XIAO_SAMD21_PLUS`
- MCU: `SAMD21G18A`
- CPU frequency baseline: `48 MHz`
- Bootloader/app offset baseline: application starts at `0x2000`

## Milestone Order
Use this exact implementation order.

### 1. Board Skeleton And Pin Map
Add the new board directory by copying the exact file shape of `SEEED_XIAO_SAMD21`.

Required files:
- `board.json`
- `mpconfigboard.h`
- `mpconfigboard.mk`
- `pins.csv`

Tasks:
- duplicate the existing XIAO SAMD21 board definition into the new board directory
- rename board identifiers to the plus board
- preserve the existing SAMD21 board structure unless the target repo already requires extra board-local files
- keep changes scoped to the new board where possible

Verification:
- the board appears as a valid target in the SAMD build system
- the new board files parse and integrate without breaking sibling boards

Commit message target:
- `samd: add XIAO SAMD21 Plus board skeleton`

### 2. Build Fixes And First Successful Firmware Build
Inspect the current `ports/samd` build flow and make only the changes required for `SEEED_XIAO_SAMD21_PLUS` to build.

Tasks:
- confirm the correct board selection command for the repo state
- inspect `mpconfigboard.mk` values used by `SEEED_XIAO_SAMD21` and nearest SAMD21 boards
- align MCU, linker, and board metadata with the plus board
- check whether default peripheral IDs are defined through board macros, and set them when supported

Verification:
- full firmware build succeeds for `SEEED_XIAO_SAMD21_PLUS`
- no unrelated board definitions are modified unless absolutely required

Commit message target:
- `samd: build MicroPython for XIAO SAMD21 Plus`

### 3. UF2 Generation Path
Determine the repo’s real UF2 path before editing. Do not assume the path is identical to another port.

Tasks:
- inspect whether UF2 is produced directly from the SAMD build or through `ports/samd/mboot`
- if `mboot` board descriptors are required, add a matching board definition for `SEEED_XIAO_SAMD21_PLUS`
- align UF2 metadata, family settings, and flash offset with the SAMD21 plus boot flow
- document the exact command sequence to produce the firmware UF2
- record the expected output path and artifact name

Verification:
- a UF2 artifact is produced
- artifact size and layout are plausible for the SAMD21 plus flash map
- build instructions are reproducible from a clean tree

Commit message target:
- `samd: add UF2 build path for XIAO SAMD21 Plus`

### 4. Serial Test Sample
Add one MicroPython sample in a repo-appropriate examples or tests location that runs as a serial command loop.

Behavior requirements:
- print a menu on start
- wait for serial commands
- execute one test at a time
- print clear `PASS` or `FAIL`
- return to idle command mode after each test
- catch exceptions and restore pin state before returning to idle

Required commands:
- `help`: print menu
- `id`: print board and firmware information
- `pinmap`: print the logical pin map used by the harness
- `led`: blink built-in LED on `D13`
- `txrxled`: toggle `D11` and `D12`
- `gpio`: validate safe user GPIO output and input behavior
- `adc`: read and print `A0..A10`
- `i2c-scan`: scan on `D4/D5`
- `spi-loop`: loopback test on `D8/D9/D10`
- `uart`: loopback test on `D6/D7`
- `pwm`: test PWM on at least one supported plus pin
- `reset`: restore harness state and return to idle

Test safety rules:
- clearly mark commands that require jumpers
- do not drive USB pins or boot-critical pins
- do not permanently reserve pins after a test completes
- keep the idle loop non-blocking except while a command is actively running

Verification:
- script parses and runs under MicroPython
- command loop returns to idle after each test
- loopback tests fail clearly when jumpers are missing

Commit message target:
- `examples: add XIAO SAMD21 Plus serial validation sample`

### 5. Final Validation And Documentation Cleanup
Tasks:
- run a clean rebuild
- confirm documented commands and paths still match the repo
- update progress log with final state
- keep final documentation concise and execution-oriented

Verification:
- clean rebuild succeeds
- UF2 path remains valid
- sample script remains runnable
- progress log accurately reflects all milestones

Commit message target:
- `docs: finalize XIAO SAMD21 Plus porting guide`

## Required Pin And Interface Exposure
The plus board must expose both base GPIO aliases and added interface pins.

### Standard Names To Expose
- `D0..D10`
- `A0..A10`
- `LED` on `D13`
- RX LED on `D12`
- TX LED on `D11`
- `SDA` on `D4`
- `SCL` on `D5`
- `TX` on `D6`
- `RX` on `D7`
- `SCK` on `D8`
- `MISO` on `D9`
- `MOSI` on `D10`

### ArduinoCore-Derived Mapping
- `A0_D0` -> `PA02`
- `A1_D1` -> `PA04`
- `A2_D2` -> `PA10`
- `A3_D3` -> `PA11`
- `A4_D4` -> `PA08`
- `A5_D5` -> `PA09`
- `A6_D6` -> `PB08`
- `A7_D7` -> `PB09`
- `A8_D8` -> `PA07`
- `A9_D9` -> `PA05`
- `A10_D10` -> `PA06`
- `USER_LED` -> `PA17`
- `RX_LED` -> `PA18`
- `TX_LED` -> `PA19`

### Peripheral Defaults
Inspect whether the SAMD port supports board-default peripheral IDs or pin macros for:
- UART
- I2C
- SPI

If supported, configure defaults so user code can instantiate the intended buses without manual pin remapping.

Baseline expectations from the current XIAO SAMD21 board:
- default UART ID `4`
- default I2C ID `2`
- default SPI ID `0`

Do not expose `USB_DM`, `USB_DP`, `SWCLK`, or `SWDIO` to Python unless the existing board convention already exposes them and there is a clear need.

## Build Guidance
Before changing build files, inspect:
- `ports/samd/boards/SEEED_XIAO_SAMD21/*`
- sibling SAMD21 board definitions
- `ports/samd/deploy.md`
- any UF2 or `mboot` files currently used by the SAMD port

Document in code comments only where behavior would otherwise be unclear. Avoid comment noise.

## Progress Log Rules
Every verified milestone must append a new section to `SAMD21_PLUS_PORTING_PROGRESS.md` with:
- timestamp
- branch
- commit hash
- milestone name
- files changed
- verification performed
- result
- blockers
- next action

Do not batch multiple milestones into one progress entry.

## Acceptance Criteria
The work is complete only when all of the following are true:
- `SEEED_XIAO_SAMD21_PLUS` exists as a selectable SAMD build target
- firmware builds successfully for the new board
- all required plus pins and interfaces are exposed correctly
- MicroPython can use the intended I2C, SPI, and UART pins with board defaults if the port supports them
- a flashable UF2 artifact is produced by documented commands
- the serial validation script runs and returns to idle after each command
- all milestone commits are pushed to the remote branch
- `SAMD21_PLUS_PORTING_PROGRESS.md` reflects the full sequence of verified work

## Suggested Initial Commands
Use the repo’s actual commands after inspection, but begin with this sequence:

```powershell
git checkout -b xiao_samd21_plus_support
Get-ChildItem ports\samd\boards\SEEED_XIAO_SAMD21
Get-Content ports\samd\boards\SEEED_XIAO_SAMD21\mpconfigboard.h
Get-Content ports\samd\boards\SEEED_XIAO_SAMD21\pins.csv
Get-Content ports\samd\deploy.md
```

## Boundaries
- Do not rename or alter the existing `SEEED_XIAO_SAMD21` board unless required to fix shared infrastructure.
- Do not mix unrelated cleanup into this effort.
- Do not skip verification before commit.
- Do not skip progress logging after a verified slice.
