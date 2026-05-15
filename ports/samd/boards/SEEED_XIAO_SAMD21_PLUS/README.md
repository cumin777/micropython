# SEEED_XIAO_SAMD21_PLUS 使用与验证说明

本文档用于指导 `SEEED_XIAO_SAMD21_PLUS` 板卡的 MicroPython 固件构建、UF2 刷写和上板功能验证。

如果你当前的目标是确认这块板子的 MicroPython 适配是否正常，建议严格按本文档的顺序执行：
- 先编译固件
- 再刷入 UF2
- 再连接串口
- 最后运行串口验证脚本逐项测试

## 1. 板卡概要

- MCU: `SAMD21G18A`
- 默认主频: `48 MHz`
- 应用起始偏移: `0x2000`
- 默认总线配置:
  - `UART(4)` 使用 `D6`/`D7`
  - `I2C(2)` 使用 `D4`/`D5`
  - `I2C(1)` 使用 `SDA1`/`SCL1`
  - `SPI(0)` 使用 `D8`/`D9`/`D10`
- 板载资源:
  - 主 LED: `LED` / `D13` / `PA17`
  - RGB LED 数据脚: `RGB_LED` / `D11` / `PA27`
  - 辅助 LED: `RX_LED` / `D12` / `PA18`
  - 按键: `BUTTON` / `PB22`

本板在 MicroPython 中应重点验证以下内容：
- 板卡目标可正常编译
- 可生成 `firmware.uf2`
- 板子可通过 UF2 正常刷机
- 基础 GPIO、LED、ADC、PWM 工作正常
- `I2C0`、`I2C1`、`SPI`、`UART` 的默认引脚映射正确
- `RGB_LED` 和 `BUTTON` 的板级别名正确

## 2. 代码位置

本板相关文件位于：

- 板卡定义目录:
  `ports/samd/boards/SEEED_XIAO_SAMD21_PLUS`
- 串口验证脚本:
  `examples/hwapi/xiao_samd21_plus_serial_validation.py`

## 3. 编译环境准备

建议在支持 `make` 和 `arm-none-eabi-gcc` 的环境下编译，例如：
- Linux
- WSL
- 已安装 GNU Arm Embedded Toolchain 的 MSYS2 / 类 Unix 环境

当前仓库在这台机器上的实际可用编译路径是：
- Windows 宿主机下只有 `wsl.exe`
- `make`、`arm-none-eabi-gcc`、`python3` 实际在 WSL 环境中可用

因此，如果你和我当前使用的是同一台机器，建议优先使用 WSL 编译，而不是直接在 PowerShell 中执行 `make`。

至少需要确认以下工具可用：

```sh
make --version
arm-none-eabi-gcc --version
python --version
```

如果 `arm-none-eabi-gcc` 不存在，MicroPython 的 `samd` 端口无法完成固件编译。

如果你在 Windows PowerShell 中执行 `make` 提示找不到命令，这是正常现象，因为当前宿主机没有直接提供 Windows 版 `make`。

## 4. 编译步骤

在仓库根目录执行：

```sh
make -C mpy-cross
make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS submodules
make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS clean
make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS
```

如果你当前在 Windows 下操作，推荐直接使用下面这组命令：

```powershell
wsl.exe -e sh -lc "cd /mnt/d/workspace/micropython-git && make -C mpy-cross"
wsl.exe -e sh -lc "cd /mnt/d/workspace/micropython-git && make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS submodules"
wsl.exe -e sh -lc "cd /mnt/d/workspace/micropython-git && make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS clean"
wsl.exe -e sh -lc "cd /mnt/d/workspace/micropython-git && make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS -j1"
```

如果你想减少并发构建带来的干扰，建议先使用单线程：

```sh
make -C ports/samd BOARD=SEEED_XIAO_SAMD21_PLUS -j1
```

本板在当前机器上的实际成功构建也是使用 `-j1` 完成的。

## 5. 预期产物

编译成功后，应看到以下文件：

- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.elf`
- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.bin`
- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.elf.map`
- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.uf2`

其中你实际刷机最常用的是：

- `ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.uf2`

当前这次实际编译生成的文件大小如下：

- `firmware.elf`: `2752112` 字节
- `firmware.bin`: `187180` 字节
- `firmware.uf2`: `374784` 字节

如果这些文件不存在，说明编译并未真正完成。

## 5.1 当前机器上的实际编译结果

本次在当前环境中已完成一次重新编译，命令执行成功，关键输出如下：

- `Converted to uf2, output size: 374784, start address: 0x2000`
- `Wrote 374784 bytes to build-SEEED_XIAO_SAMD21_PLUS/firmware.uf2`

当前可用固件路径是：

- `D:\workspace\micropython-git\ports\samd\build-SEEED_XIAO_SAMD21_PLUS\firmware.uf2`

对应 ELF 和 BIN 路径是：

- `D:\workspace\micropython-git\ports\samd\build-SEEED_XIAO_SAMD21_PLUS\firmware.elf`
- `D:\workspace\micropython-git\ports\samd\build-SEEED_XIAO_SAMD21_PLUS\firmware.bin`

产物最后生成时间为：

- `2026-05-15 20:24:58`

## 6. UF2 说明

当前 `samd` 端口是直接通过 `tools/uf2conv.py` 生成 UF2，不依赖额外的独立打包流程。

本板当前对应的关键 UF2 参数为：

- UF2 family: `0x68ed2b88`
- UF2 base address: `0x2000`

如果你后续发现刷机后无法启动、启动后异常复位或固件不运行，需要优先回查：
- `mpconfigboard.mk` 中的偏移是否仍为 `0x2000`
- `ports/samd/mcu/samd21/mpconfigmcu.mk` 中的 UF2 family 是否未被错误修改

## 6.1 本次编译观察到的容量情况

本次 `arm-none-eabi-size` 输出为：

```text
text    data    bss     dec     hex
187056  124     2224    189404  2e3dc
```

链接阶段同时给出了区域占用：

```text
FLASH: 187180 B / 184 KB  (99.34%)
RAM:     2352 B / 32 KB   (7.18%)
```

这说明：
- 当前固件可以成功编译
- 当前固件已经非常接近 `SAMD21` 的 Flash 上限

如果你后续继续往这个板子里加模块、冻结脚本或打开更多功能，极有可能因为 Flash 超限而编译失败。后续若出现此类问题，应优先从裁剪功能和精简配置入手，而不是先怀疑工具链。

## 7. 刷写步骤

### 7.1 进入 bootloader

1. 将板子通过 USB 连接到电脑。
2. 快速连续按两次复位键。
3. 等待电脑上出现一个 UF2 U 盘设备。

如果没有出现 UF2 盘：
- 检查当前板子是否已经有可用 bootloader
- 更换 USB 线
- 更换 USB 接口
- 确认不是仅充电线

### 7.2 复制固件

将下面这个文件复制到 UF2 盘中：

`ports/samd/build-SEEED_XIAO_SAMD21_PLUS/firmware.uf2`

### 7.3 观察刷机结果

正常情况下：
- 文件复制完成后，UF2 盘会自动消失
- 板子会自动重启
- 系统会重新枚举出新的串口设备

如果 UF2 盘复制后没有消失，或者板子没有重启，说明刷写未正常完成，需要重新检查 UF2 文件与 bootloader。

## 8. 串口连接

刷机完成后，打开串口终端连接开发板。

常用工具包括：
- `mpremote`
- `thonny`
- `MobaXterm`
- `PuTTY`
- `screen`
- `minicom`

如果你只想快速确认设备可通信，建议先用：

```sh
mpremote connect auto
```

如果连接成功，可以看到 MicroPython REPL 提示符：

```text
>>>
```

## 9. 运行验证脚本

验证脚本文件：

`examples/hwapi/xiao_samd21_plus_serial_validation.py`

你可以用两种方式运行。

### 方式 A：直接复制脚本内容到 REPL

适合快速试验，但不适合长脚本反复测试。

### 方式 B：使用 `mpremote` 执行

推荐方式，例如：

```sh
mpremote connect auto fs cp examples/hwapi/xiao_samd21_plus_serial_validation.py :
mpremote connect auto run examples/hwapi/xiao_samd21_plus_serial_validation.py
```

如果你已经复制到板子上，也可以进入 REPL 后执行：

```python
import xiao_samd21_plus_serial_validation
```

脚本启动后会打印命令菜单，并进入等待命令状态。

正常启动时你应看到类似输出：

```text
XIAO SAMD21 PLUS test
h help
...
idle
>
```

## 10. 验证命令总览

当前脚本为了适应 `SAMD21` 的内存限制，使用的是精简的单字母命令：

- `h`: 帮助
- `i`: 板卡信息
- `l`: 主 LED
- `t`: `RGB_LED + RX_LED` 同步闪烁
- `n`: RGB LED 颜色切换
- `g`: GPIO
- `a`: ADC
- `c`: `I2C(2)`，即 `D4/D5`
- `v`: `I2C(1)`，即 `SDA1/SCL1`
- `s`: SPI 回环测试
- `u`: UART 回环测试
- `p`: PWM
- `b`: 读取按键
- `r`: reset

每次命令执行结束后，脚本应回到：

```text
idle
cmd>
```

如果脚本执行完某条命令后没有回到等待状态，说明脚本逻辑或底层驱动可能存在问题。

## 11. 逐项验证说明

### 11.1 `h`

用途：
- 打印帮助菜单

预期结果：
- 能看到全部支持命令
- 返回 `idle`

### 11.2 `i`

用途：
- 打印板卡名称、固件信息、Python 版本、主频

预期结果：
- 能打印板卡名和当前主频

如果 `Board` 名称不对，说明板卡定义可能没有正确生效。

### 11.3 `l`

用途：
- 闪烁主 LED

预期结果：
- 主 LED 闪烁 3 次

### 11.4 `t`

用途：
- 同时闪烁 `RGB_LED` 数据脚和 `RX_LED`

预期结果：
- `RX_LED` 会闪烁
- `RGB_LED` 对应外设如果存在，也会出现响应

这个命令主要用于快速确认新设备树中的 `RGB_LED` / `RX_LED` 别名是否能正常解析。

### 11.5 `n`

用途：
- 测试板载 RGB LED

预期结果：
- RGB LED 依次切换几种颜色，然后熄灭
- 串口输出 `rgb ok`

说明：
- 当前实现假设 `PA27` 挂载的是 `WS2812/NeoPixel` 类单总线 RGB 灯
- 如果颜色顺序和实际硬件不一致，可能会“亮色不对”，但这依然说明信号路径是通的

### 11.6 `g`

用途：
- 验证安全 GPIO 输出逻辑

当前脚本测试引脚：
- `D0`
- `D1`
- `D2`
- `D3`

预期结果：
- 串口打印类似 `('D0', 1)` 这样的状态
这个测试主要验证脚本可以正常驱动这些基础 GPIO。

### 11.7 `a`

用途：
- 读取 `A0..A10`

预期结果：
- 会打印 11 路 ADC 值
即使没有外部信号，数值变化也可能正常，关键是每路都能读取。

如果某几路固定异常或报错，优先检查：
- `pins.csv` 中的别名是否正确
- 该引脚在当前板级定义中是否支持 ADC

### 11.8 `c`

用途：
- 使用 `I2C(2)` 在 `D4/D5` 上扫描设备

预期结果：
- 输出类似 `i2c []`
- 即使没有挂设备，空列表也是正常的

判定重点：
- 命令能执行完
- 没有抛异常
- 总线初始化成功

如果你挂了 I2C 设备，也可以借此确认设备地址是否可见。

### 11.9 `v`

用途：
- 使用第二组 I2C 在 `SDA1/SCL1` 上扫描设备

预期结果：
- 输出类似 `i2c1 []`
- 即使没有挂设备，空列表也是正常的

这个测试用于确认新设备树中新增的第二组 I2C 别名是否正确。

### 11.10 `s`

用途：
- 验证 `SPI(0)` 的默认引脚映射

测试前必须加跳线：
- `D10 -> D9`

含义：
- `D10` 是 `MOSI`
- `D9` 是 `MISO`
- `D8` 是时钟 `SCK`

预期结果：
- 输出类似 `spi b'SPI'`
- 接收内容应与发送内容一致

如果未接跳线，通常会 `FAIL`，这是预期行为，不代表 SPI 初始化本身失败。

### 11.11 `u`

用途：
- 验证 `UART(4)` 的默认引脚映射

测试前必须加跳线：
- `D6 -> D7`

含义：
- `D6` 是 `TX`
- `D7` 是 `RX`

预期结果：
- 输出类似 `uart b'UART\\r\\n'`
- 收到的数据应与发送内容一致

如果未接跳线，通常会 `FAIL`，这是预期现象。

### 11.12 `p`

用途：
- 在 `D1` 上输出 PWM

预期结果：
- 串口输出 `pwm ok`

这个测试当前主要验证：
- PWM 对象可创建
- 指定引脚能初始化为 PWM

如果你有示波器或逻辑分析仪，可以进一步确认波形。

### 11.13 `b`

用途：
- 读取 `BUTTON`

预期结果：
- 串口输出类似 `button 0` 或 `button 1`

这个命令用于确认新设备树中新增的 `BUTTON` 别名有效。

### 11.14 `r`

用途：
- 清理脚本内部已占用的资源，并回到等待状态

预期结果：
- 输出 `reset ok`
- 回到 `idle`

如果你前面某项测试后怀疑引脚未释放，可先执行一次 `reset`。

## 12. 推荐验证顺序

建议第一次上板时按这个顺序验证：

1. `i`
2. `l`
3. `t`
4. `n`
5. `g`
6. `a`
7. `c`
8. `v`
9. `b`
10. `p`
11. 接上 `D10 -> D9`，执行 `s`
12. 接上 `D6 -> D7`，执行 `u`
13. `r`

这个顺序的目的：
- 先验证不依赖外部跳线的能力
- 最后再验证需要物理回环的接口

## 13. 常见问题排查

### 13.1 能编译，但刷入后没有 REPL

优先检查：
- 是否真的刷入了 `firmware.uf2`
- 板子是否自动重启
- USB 线是否支持数据通信
- 操作系统是否重新枚举出串口

### 13.2 `id` 显示的板名不对

优先检查：
- 当前刷入的是否是 `SEEED_XIAO_SAMD21_PLUS` 的固件
- 是否误刷了其他 `samd` 板卡的 UF2

### 13.3 `i2c-scan` 报错

优先检查：
- `D4` / `D5` 是否被外部电路强拉
- 外设供电和地是否正确
- 是否有引脚定义与当前硬件不一致

### 13.4 `spi-loop` 失败

优先检查：
- 是否真的接了 `D10 -> D9`
- 跳线是否接触不良
- 是否误把 `D8` 也接错

### 13.5 `uart` 失败

优先检查：
- 是否真的接了 `D6 -> D7`
- 波特率是否与脚本一致，当前是 `115200`
- 是否有其他外设占用了该串口

### 13.6 `adc` 某几路异常

优先检查：
- 该引脚在板级定义中是否真的映射为 ADC
- 是否被外设占用
- 是否存在悬空输入导致读数不稳定

## 14. 建议记录方式

建议每次验证时记录以下内容：

- 使用的固件提交 hash
- 编译时间
- 刷写是否成功
- `i` 输出
- `c` / `v` 输出
- `n` 的 RGB 响应
- `s` 是否加了 `D10 -> D9` 跳线
- `u` 是否加了 `D6 -> D7` 跳线
- 每项命令的 PASS/FAIL 结果

如果后续需要回归测试，这些记录会非常有用。

## 15. 当前验证结论边界

本文档指导的是：
- 如何验证这块板子的 MicroPython 移植结果是否基本正常

本文档不等价于：
- 所有外设都已完成长期稳定性验证
- 所有模拟通道都已完成精度校准
- 所有边界场景都已覆盖

如果你要继续做更深入验证，下一步建议补充：
- 外接 I2C 真实器件测试
- 外接 SPI 真实器件测试
- UART 长时间收发测试
- ADC 多通道对比测试
- PWM 波形仪器测量
