# Robotické rameno Typhoon

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![sk](https://img.shields.io/badge/lang-sk-green.svg)](README.sk.md)

`typhoon-robotic-arm` je Python knižnica, ktorá umožňuje ovládanie robotického ramena Typhoon. Táto knižnica poskytuje rôzne funkcie vrátane výpočtov, komunikácie a pohybu ramena.

## Inštalácia

Potrebný je **Python 3.8+**. Najnovšiu verziu stiahneš týmto príkazom:

```bash
pip install pyserial
pip install typhoon-robotic-arm
```

## Quickstart

```python
from typhoon import Typhoon

typhoon = Typhoon("COM3", 130, 0, 0, output=True)

typhoon.move_to(100, 0, 0)
typhoon.activate_tool(pw9=255)
typhoon.move_to(0, 0, 0)

typhoon.close()
```

## Typhoon class

Core developement interface for Typhoon.

| Argument | Description |
| :--- | :--- |
| port (required) | Port on which is typhoon robotic arm connected. You can check this in your Device Manager on Windows under USB Connector Managers. |
| start_x (required) | Startring X position of robotic arm. |
| start_y (required) | Startring Y position of robotic arm. |
| start_z (required) | Startring Z position of robotic arm. |
| tool_x | X offset of the tool. |
| tool_y | Y offset of the tool. |
| tool_z | Z offset of the tool. |
| output | If you want to see output from the Arduino board. |