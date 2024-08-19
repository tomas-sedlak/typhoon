# Typhoon

Typhoon is our school project robotic arm. You can implement it in your code or create custom GUI with our library.

## Quickstart

This guide will walk you through the basic usage of typhoon.

Let's get started with some examples.

### Moving the arm

Begin by importing the [Typhoon class](#typhoon-class)

```python
from typhoon import Typhoon
```

Now, let's connect to the physical Typhoon robotic arm:

```python
typhoon = Typhoon("COM3", 130, 0, 0, output=True)
```

Now we have `Typhoon` object called `typhoon`.

After that we can move our robotic arm to a specific coordinates x, y, z:

```python
typhoon.move_to(100, 0, 0)
```

At the end of the code it's recommended to call `close()` function to end connection:

```python
typhoon.close()
```

This is how our full code looks like:

```python
from typhoon import Typhoon

typhoon = typhoon.Typhoon("COM3", 130, 0, 0, output=True)
typhoon.move_to(100, 0, 0)
typhoon.close()
```

## Typhoon object

Core developer interface for typhoon.

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

## Creating custom Typhoon GUI

```
- components
    - custom_component.py
    - ...
- data
    - data.csv
    - data.json
    - ...
- pages
    - home_page.py
    - settings_page.py
    - ...
- main.py
- config.json
```

Contents of `config.json` file:

```json
{
    "name": "Typhoon Chess",
    "icon": "play_circle",
    "version": "1.0.0",
    "author": "Fname Lname <email@example.com>"
}
```