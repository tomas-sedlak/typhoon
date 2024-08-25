import sys
import time
from typhoon.utils import bcolors
from typhoon.utils import Calculations
from typhoon.utils import Communication

try:
    import serial
except ImportError:
    print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Library pyserial not found.")
    print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Install it with: {bcolors.WARNING}pip install pyserial{bcolors.ENDC}")
    sys.exit(0)

class Typhoon():
    """Controls a Typhoon robotic arm through serial communication."""

    def __init__(self, port: str, start_x: int, start_y: int, start_z: int,
                 tool_x: int = 0, tool_y: int = 0, tool_z: int = 0,
                 output: bool = False) -> None:
        """
        Initializes the Typhoon robotic arm object with serial port and starting position.

        Args:
            port: Serial port to connect to the arm (e.g., COM10).
            start_x: Initial X coordinate.
            start_y: Initial Y coordinate.
            start_z: Initial Z coordinate.
            tool_x: Offset of the tool in X from the arm center (default 0).
            tool_y: Offset of the tool in Y from the arm center (default 0).
            tool_z: Offset of the tool in Z from the arm center (default 0).
            output: Enable printing debug messages (default False).
            length_upper_arm: Length of the upper arm (default 215).
            length_lower_arm: Length of the lower arm (default 250).
        """

        try:
            self.serial = serial.Serial(port, 115200)
            self.serial.flushInput()
            time.sleep(1.5)
            print(f"{bcolors.OKGREEN}[SUCCESS]{bcolors.ENDC} Successfully connected through port {bcolors.WARNING}'{port}'{bcolors.ENDC}!")
        except serial.serialutil.SerialException:
            print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Could not open port {bcolors.WARNING}'{port}'{bcolors.ENDC}.")
            print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Try a different port or check if the cable is connected.")
            sys.exit(0)

        self.x, self.y, self.z = start_x, start_y, start_z
        self.base_angle, self.upper_angle, self.lower_angle = 0, 0, 0
        self.start_base_angle, self.start_upper_angle, self.start_lower_angle = Calculations.angles_from_coords(self.x, self.y, self.z)

        self.START_X, self.START_Y, self.START_Z = start_x, start_y, start_z
        self.OUTPUT = output

    def move_to(self, x: int, y: int, z: int) -> None:
        """Moves the arm to the specified coordinates."""

        self.x, self.y, self.z = self.START_X + x, self.START_Y + y, self.START_Z + z
        self.base_angle, self.upper_angle, self.lower_angle = Calculations.angles_from_coords(self.x, self.y, self.z)

        base_angle = Calculations.steps_from_angles(self.base_angle - self.start_base_angle)
        upper_angle = Calculations.steps_from_angles(self.upper_angle - self.start_upper_angle)
        lower_angle = Calculations.steps_from_angles(self.lower_angle - self.start_lower_angle)

        Communication.send(self.serial, "coords", f"{base_angle},{lower_angle},{upper_angle}", output=self.OUTPUT)

    def activate_tool(self, pw8: int = 0, pw9: int = 0, pw10: int = 0) -> None:
        """
        Sets the state of the tool (e.g., gripper open/close, suction on/off).

        Args:
            state: Dictionary with tool names as keys and desired states (True/False) as values.
        """
        Communication.send(self.serial, "powers", f"{pw8},{pw9},{pw10}", output=self.OUTPUT)

    def get_angles(self) -> tuple[int, int, int]:
        """Returns the current base, upper, and lower arm angles."""
        return self.base_angle, self.upper_angle, self.lower_angle

    def get_coords(self) -> tuple[int, int, int]:
        """Returns the current X, Y, and Z coordinates of the arm tip."""
        return self.x, self.y, self.z

    def send_file(self, file_path: str, separator: str = " ") -> None:
        """Moves the arm according to coordinates specified in a text file."""
        data_file = open(file_path, "r")

        try:
            for line in data_file:
                items = line.strip().split(separator)
                float_items = [float(item) for item in items]
                self.move_to(*float_items)
        except FileNotFoundError:
            print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} File not found: {bcolors.WARNING}'{file_path}'{bcolors.ENDC}.")
        except ValueError:
            print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Error parsing line in file {bcolors.WARNING}'{file_path}'{bcolors.ENDC}. Check the data format.")

    def close(self) -> None:
        """Closes the serial connection."""
        self.serial.close()
