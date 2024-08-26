# Typhoon Robotic Arm

`typhoon-robotic-arm` is a Python library that enables control of the Typhoon robotic arm. This library provides various functionalities, including calculations, communication and movement of the arm.

## Installation

Requires **Python 3.8+**. Download and install the latest release:

```bash
pip install pyserial
pip install -i https://test.pypi.org/simple/ typhoon-robotic-arm
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