# Typhoon Robotic Arm

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![sk](https://img.shields.io/badge/lang-sk-green.svg)](README.sk.md)

`typhoon-robotic-arm` is a Python library that enables control of the Typhoon robotic arm. This library provides various functionalities, including calculations, communication and movement of the arm.

## Installation

Requires **Python 3.8+**. Download and install the latest release:

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

## References

*class* **Typhoon**(*port: str, start_x: int, start_y: int, start_z: int, tool_x: int = 0, tool_y: int = 0, tool_z: int = 0, output: bool = False*)

- Controls a Typhoon robotic arm through serial communication. Offers a user-friendly interface for various arm operations.

- **Parameters:**

    - **port** (*required*) - Port on which is typhoon robotic arm connected. You can check this in your Device Manager on - Windows under USB Connector Managers.
    - **start_x** (*required*): - Startring X position of robotic arm.
    
    - **start_y** (*required*) - Startring Y position of robotic arm.
    
    - **start_z** (*required*) - Startring Z position of robotic arm.
    
    - **tool_x** - X offset of the tool.
    
    - **tool_y** - Y offset of the tool.
    
    - **tool_z** - Z offset of the tool.
    
    - **output** - If you want to see output from the Arduino board.


- **Methods:**

    - **goto**(*x: int, y: int, z: int*):
        - Moves the arm to the specified coordinates.
        - Calculates the required angles and sends them to the arm.

    - **tool**(*pw8: int = 0, pw9: int = 0, pw10: int = 0*):

        - Controls the state of the tool (e.g., gripper open/close, suction on/off).
        - Sends PWM values to the arm to activate the desired tool functions.

    - **get_angles**():

        - Returns the current base, upper, and lower arm angles as a tuple.

    - **get_coords**():

        - Returns the current X, Y, and Z coordinates of the arm tip as a tuple.

    - **send_file**(*file_path: str, separator: str = " "*):

        - Moves the arm according to coordinates specified in a text file.
        - Each coordinate must be written on **new line** in format `x y z`.
        - When you set `separator` to `, `, program expects on each line data in format `x, y, z`

    - **close**():

        - Closes the serial connection to the arm.