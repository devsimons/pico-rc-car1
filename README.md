# Pico RC Car - WiFi Controlled

WiFi-controlled RC car using Raspberry Pi Pico W with web-based interface.

## Requirements

**Firmware**: MicroPython for Raspberry Pi Pico W
- Download from [micropython.org](https://micropython.org/download/RPI_PICO_W/)
- Flash using Thonny IDE or drag-and-drop bootloader method

## Hardware

**Motor Driver**: TB6612FNG dual motor driver
- Motor A: Drive motor (forward/backward)
- Motor B: Steering motor (left/right)
- Standby: GPIO 6 (active high)

**Pin Configuration**:
```
Motor A (Drive):    AIN1=GPIO0, AIN2=GPIO1, PWMA=GPIO2
Motor B (Steering): BIN1=GPIO3, BIN2=GPIO4, PWMB=GPIO5
Headlights:         LED1=GPIO7, LED2=GPIO8
```

**Power**: 3x AA batteries (4.5V)
- VM (motor power) and VSYS from battery positive
- VCC (logic) from Pico 3.3V output

**PWM**: 1000 Hz, 16-bit duty cycle (65535 full speed)

## Network

**WiFi AP**:
- SSID: `RC-Car`
- Password: `12345678`
- IP: `192.168.4.1`

## Control

Web interface at `http://192.168.4.1`

**Commands**:
- `forward` / `reverse` - Drive motor, LEDs on
- `left` / `right` - Steering motor
- `center` - Center steering
- `stop` - Stop all, LEDs off

Touch/mouse press activates, release auto-stops/centers.

## Usage

1. Power on Pico W
2. Connect to "RC-Car" WiFi
3. Browse to `http://192.168.4.1`
4. Control via web buttons

## Wiring Diagram

```mermaid
graph LR
        subgraph Battery["Battery Pack (3x AA = 4.5V)"]
            BATT_POS["Battery +"]
            BATT_NEG["Battery -"]
        end

        subgraph Pico["Raspberry Pi Pico W H"]
            GP0["GP0"]
            GP1["GP1"]
            GP2["GP2 (PWMA)"]
            GP3["GP3"]
            GP4["GP4"]
            GP5["GP5 (PWMB)"]
            GP6["GP6 (STBY)"]
            GP7["GP7 (LED1)"]
            GP8["GP8 (LED2)"]
            PICO_3V3["3.3V (Pin 36)"]
            PICO_VSYS["VSYS (Pin 39)"]
            PICO_GND["GND"]
        end

        subgraph TB6612["TB6612FNG Motor Driver"]
            VM["VM (Motor Power)"]
            VCC["VCC (Logic Power)"]
            GND["GND"]
            STBY["STBY"]
            AIN1["AIN1"]
            AIN2["AIN2"]
            PWMA["PWMA"]
            BIN1["BIN1"]
            BIN2["BIN2"]
            PWMB["PWMB"]
            AO1["AO1"]
            AO2["AO2"]
            BO1["BO1"]
            BO2["BO2"]
        end

        subgraph Motors["Motors"]
            MOTOR_A["Drive Motor"]
            MOTOR_B["Steering Motor"]
        end

        subgraph LEDs["Headlights"]
            LED1["LED 1"]
            LED2["LED 2"]
        end

        BATT_POS -->|Red Wire| VM
        BATT_POS -->|Red Wire| PICO_VSYS
        BATT_NEG -->|Black Wire| GND
        BATT_NEG -->|Black Wire| PICO_GND
        PICO_3V3 -->|Red Wire| VCC

        GP0 -->|Blue Wire| AIN1
        GP1 -->|Yellow Wire| AIN2
        GP2 -->|Green Wire| PWMA

        GP3 -->|Blue Wire| BIN1
        GP4 -->|Yellow Wire| BIN2
        GP5 -->|Green Wire| PWMB

        GP6 -->|Purple Wire| STBY

        AO1 -->|Motor Wire| MOTOR_A
        AO2 -->|Motor Wire| MOTOR_A
        BO1 -->|Motor Wire| MOTOR_B
        BO2 -->|Motor Wire| MOTOR_B

        GP7 -->|Wire + Resistor| LED1
        GP8 -->|Wire + Resistor| LED2
        LED1 -->|To GND| PICO_GND
        LED2 -->|To GND| PICO_GND

        style Battery fill:#ff6b6b
        style Pico fill:#2f9e44
        style TB6612 fill:#c92a2a
        style Motors fill:#666
        style LEDs fill:#ffd43b
```
