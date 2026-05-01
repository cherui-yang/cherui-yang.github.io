# 03 - 单片机入门：Arduino

> 预计时间：1-2 个月  
> 目标：快速体验单片机开发，理解 GPIO、PWM、ADC、UART 等外设概念

## 为什么用 Arduino？

- 上手极快，社区资料极多
- 适合零硬件基础的同学建立信心
- 但**不要止步于 Arduino 库**，后续要尝试直接操作寄存器

## 1. Arduino 基本使用

### 开发板推荐

- Arduino UNO（基于 ATmega328P，约 ¥100）
- 兼容板（如 Keyes、DFRobot 的 UNO R3）

### 核心函数

- `pinMode()`, `digitalWrite()`, `digitalRead()`
- `analogWrite()`（PWM）
- `analogRead()`（ADC）
- `Serial.begin()`, `Serial.print()`

### 🛠️ 基础项目

1. **LED 呼吸灯**（PWM 调光）
2. **按键控制蜂鸣器**（外部中断初体验）
3. **温湿度传感器 DHT11**（单总线协议）
4. **OLED 显示屏显示字符**（I2C 接口）
5. **蓝牙遥控小车**（UART 通信 + 电机驱动 L298N）

## 2. 进阶：直接操作 AVR 寄存器

Arduino 库隐藏了底层细节。为了真正理解单片机，请尝试：

- 不使用 `digitalWrite()`，直接操作 `PORTB`、`DDRB` 寄存器控制 LED
- 不使用 `delay()`，自己写一个基于定时器中断的延时函数
- 不使用 `Serial` 对象，直接配置 `UCSR0A` 等寄存器实现串口发送

### 📘 推荐阅读

- ATmega328P 数据手册（英文，只看相关章节）
- 《Arduino 技术内幕》

## 3. 项目建议

完成一个综合性项目，例如：

- **红外遥控智能灯**：红外接收 + PWM 调光 + 按键记忆
- **超声波测距仪**：HC-SR04 + OLED 显示 + 蜂鸣器报警

> 做完 Arduino 后，你应该能熟练阅读简单的原理图，并对外设有直观认识。接下来请进入 [04-STM32进阶](./04-STM32进阶与ARM开发.md)。