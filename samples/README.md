# XIAO RP2040 Plus - MicroPython 测试指南

## 概述

本目录包含 Seeed XIAO RP2040 Plus 板卡的 MicroPython 测试脚本，用于验证所有引脚和外设功能。

## 硬件准备

### 基本要求

- Seeed XIAO RP2040 Plus 开发板 x1
- USB-C 数据线 x1

### 额外硬件（按测试项）

| 测试项 | 需要的硬件 |
|--------|-----------|
| GPIO 输出 | LED + 330 欧电阻（可选） |
| GPIO 输入 | 杜邦线（用于连接 GND/3V3） |
| ADC | 电位器或分压电路 |
| I2C0 | 任意 I2C 传感器/模块 |
| I2C1 | 任意 I2C 传感器/模块 |
| SPI 回环 | 1 根杜邦线（D10 连 D9） |
| UART 回环 | 1 根杜邦线（D6 连 D7） |
| LED | 无（板载） |
| WS2812 | 无（板载） |
| PWM | LED + 330 欧电阻（可选） |

### 跳线连接说明

```
SPI 回环测试:
  D10 (GPIO3, MOSI) ──── D9 (GPIO4, MISO)

UART 回环测试:
  D6 (GPIO0, TX) ──── D7 (GPIO1, RX)

I2C 测试:
  I2C0: SDA → D4 (GPIO6), SCL → D5 (GPIO7)
  I2C1: SDA → D14 (GPIO20), SCL → D13 (GPIO19)
```

## 测试脚本说明

### 1. test_gpio_basic.py — GPIO 输入输出测试

**覆盖引脚**: D12-D17, D19-D27（15 个新增引脚）

**测试内容**:
- 将所有新引脚设为输出模式，依次切换 HIGH/LOW
- 将所有新引脚设为输入模式（上拉），读取当前电平
- 将所有新引脚设为输入模式（下拉），读取当前电平

**预期输出**: 每个引脚输出 `OK`，上拉时读取 HIGH (1)，下拉时读取 LOW (0)

**运行**: `import test_gpio_basic`

### 2. test_adc.py — ADC 模拟输入测试

**覆盖引脚**: A0-A3 (GPIO26-29)

**测试内容**:
- 单次读取 4 个 ADC 通道的原始值和电压值
- 持续 5 秒读取所有通道，每 0.5 秒刷新

**预期输出**: 原始值 0-65535，电压值 0-3.3V

**运行**: `import test_adc`

### 3. test_i2c0.py — I2C0 总线扫描测试

**覆盖引脚**: SDA=GPIO6, SCL=GPIO7

**测试内容**:
- 初始化 I2C0 总线（400kHz）
- 扫描总线上的所有设备地址

**预期输出**: 如果连接了 I2C 设备，打印设备地址（如 `0x3C`）；否则提示未找到设备

**运行**: `import test_i2c0`

### 4. test_i2c1.py — I2C1 总线扫描测试（新增功能）

**覆盖引脚**: SDA1=GPIO20, SCL1=GPIO19

**测试内容**:
- 初始化 I2C1 总线（400kHz）
- 扫描总线上的所有设备地址
- 同时初始化 I2C0 和 I2C1，验证双总线并行工作

**预期输出**: 与 I2C0 类似，额外验证双总线同时可用

**运行**: `import test_i2c1`

### 5. test_spi.py — SPI 回环测试

**覆盖引脚**: SCK=GPIO2, MOSI=GPIO3, MISO=GPIO4

**前提**: D10 (MOSI) 与 D9 (MISO) 之间连接跳线

**测试内容**:
- 发送不同数据模式，验证接收数据一致
- 测试不同波特率（500KHz - 10MHz）

**预期输出**: 发送数据 = 接收数据时显示 `PASS`

**运行**: `import test_spi`

### 6. test_uart.py — UART 回环测试

**覆盖引脚**: TX=GPIO0, RX=GPIO1

**前提**: D6 (TX) 与 D7 (RX) 之间连接跳线

**测试内容**:
- 发送文本和二进制数据，验证回环接收
- 测试多种波特率（9600 - 115200）

**预期输出**: 发送数据 = 接收数据时显示 `PASS`

**运行**: `import test_uart`

### 7. test_led.py — 用户 LED 测试

**覆盖引脚**: GPIO25（板载用户 LED）

**测试内容**:
- LED 闪烁 5 次（间隔 0.5 秒）
- LED 快速切换模拟呼吸效果

**预期输出**: 肉眼可见 LED 闪烁和呼吸效果

**运行**: `import test_led`

### 8. test_neopixel.py — WS2812 RGB LED 测试

**覆盖引脚**: GPIO12 (数据), GPIO24 (电源使能)

**前提**: 需要先上传 `ws2812.py` 库到板卡文件系统（Seeed Studio 提供的 PIO 驱动库）

**测试内容**:
- 依次显示 8 种基本颜色（红、绿、蓝、黄、青、品红、白、灭）
- 蓝色渐变呼吸效果
- 彩虹色循环

**预期输出**: 肉眼可见 RGB LED 颜色变化和渐变效果

**运行**:
1. 先上传 `ws2812.py` 到板卡
2. `import test_neopixel`

### 9. test_pwm.py — PWM 输出测试

**覆盖引脚**: D12 (GPIO18), D19 (GPIO5), D20 (GPIO13)

**测试内容**:
- 占空比从 0% 扫描到 100% 再回到 0%
- 不同频率测试（100Hz - 100kHz）
- LED 呼吸效果（PWM 方式）

**预期输出**: 连接 LED 可见亮度变化

**运行**: `import test_pwm`

### 10. test_all_pins.py — 一键全引脚测试

**覆盖引脚**: 所有引脚（D0-D10, D12-D27, LED, NEOPIXEL, NEOPIXEL_POWER）

**测试内容**:
- 依次执行所有测试项
- 统计通过/失败数量
- 输出汇总报告

**预期输出**: 最后打印 `Results: N/N PASSED, 0/N FAILED`

**运行**: `import test_all_pins`

## 测试结果解读

### PASS
测试通过，引脚/外设工作正常。

### FAIL
测试失败，可能原因：
1. **接线错误** — 检查跳线是否连接正确
2. **外设未连接** — I2C/SPI/UART 需要外部设备或回环线
3. **引脚冲突** — 某些引脚可能被其他功能占用
4. **硬件故障** — 板卡或引脚损坏

## 故障排查

### I2C 扫描不到设备
- 检查 SDA/SCL 接线是否正确
- 确认 I2C 设备供电正常
- 尝试降低频率：`I2C(id, sda=..., scl=..., freq=100000)`

### SPI/UART 回环数据不匹配
- 确认回环跳线连接牢固
- 降低波特率重新测试

### GPIO 输入始终为 0 或 1
- 检查引脚是否被其他外设占用
- 尝试手动连接到 GND 或 3V3 验证

### WS2812 不亮
- 检查 GPIO24 (NEOPIXEL_POWER) 是否已拉高
- 注意：Plus 版本的电源引脚是 GPIO24，不是老版的 GPIO11

### 编译或导入错误
- 确认使用的是 `SEEED_XIAO_RP2040_PLUS` 目标编译的固件
- 检查固件版本是否匹配

## 引脚映射速查

| Arduino Pin | GPIO | 功能 | Arduino Pin | GPIO | 功能 |
|-------------|------|------|-------------|------|------|
| D0 / A0 | 26 | ADC0 | D15 | 21 | GPIO |
| D1 / A1 | 27 | ADC1 | D16 | 22 | GPIO |
| D2 / A2 | 28 | ADC2 | D17 | 23 | GPIO |
| D3 / A3 | 29 | ADC3 | D19 | 5 | GPIO |
| D4 / SDA | 6 | I2C0 | D20 | 13 | GPIO |
| D5 / SCL | 7 | I2C0 | D21 | 14 | GPIO |
| D6 / TX | 0 | UART | D22 | 15 | GPIO |
| D7 / RX | 1 | UART | D23 | 16 | GPIO |
| D8 / SCK | 2 | SPI | D24 | 17 | GPIO |
| D9 / MISO | 4 | SPI | D25 | 10 | GPIO |
| D10 / MOSI | 3 | SPI | D26 | 9 | GPIO |
| D12 | 18 | GPIO | D27 | 8 | GPIO |
| D13 / SCL1 | 19 | I2C1 | LED | 25 | 用户LED |
| D14 / SDA1 | 20 | I2C1 | NEOPIXEL | 12 | WS2812 |
