import sys
import time
from typhoon.utils import bcolors
from typhoon.utils import calculations
from typhoon.utils import communication

try:
    import serial
except ImportError:
    print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Library pyserial not found.")
    print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Install it with: {bcolors.WARNING}pip install pyserial{bcolors.ENDC}")
    sys.exit(0)

class Typhoon():
    """Controls a Typhoon robotic arm through serial communication."""

    def __init__(self, port: str, start_x: int, start_y: int, start_z: int,
                 tool_offset_x: int = 0, tool_offset_y: int = 0, tool_offset_z: int = 0,
                 output: bool = False) -> None:
        """
        Initializes the Typhoon robotic arm object with serial port and starting position.

        Args:
            port: Serial port to connect to the arm (e.g., COM10).
            start_x: Initial X coordinate.
            start_y: Initial Y coordinate.
            start_z: Initial Z coordinate.
            tool_offset_x: Offset of the tool in X from the arm center (default 0).
            tool_offset_y: Offset of the tool in Y from the arm center (default 0).
            tool_offset_z: Offset of the tool in Z from the arm center (default 0).
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

        self.x, self.y, self.z = 0, 0, 0
        self.joint1_angle, self.joint2_angle, self.joint3_angle = 0, 0, 0
        
        self.START_JOINT1_ANGLE, self.START_JOINT2_ANGLE, self.START_JOINT3_ANGLE = calculations.angles_from_coords(start_x, start_y, start_z)
        self.TOOL_OFFSET_X, self.TOOL_OFFSET_Y, self.TOOL_OFFSET_Z = tool_offset_x, tool_offset_y, tool_offset_z
        self.OUTPUT = output

    def move_to(self, x: int, y: int, z: int) -> None:
        """Moves the arm to the specified coordinates."""

        self.x, self.y, self.z = x - self.TOOL_OFFSET_X, y - self.TOOL_OFFSET_Y, z - self.TOOL_OFFSET_Z
        self.joint1_angle, self.joint2_angle, self.joint3_angle = calculations.angles_from_coords(self.x, self.y, self.z)

        joint1_steps = calculations.steps_from_angle(self.START_JOINT1_ANGLE - self.joint1_angle)
        joint2_steps = calculations.steps_from_angle(self.START_JOINT2_ANGLE - self.joint2_angle)
        joint3_steps = calculations.steps_from_angle(self.START_JOINT3_ANGLE - self.joint3_angle) - joint2_steps # na tomto sme stravili 4 dni!!!
        
        communication.send(self.serial, "coords", f"{joint1_steps},{joint2_steps},{joint3_steps}", output=self.OUTPUT)

    def move_home(self) -> None:
        """Moves the arm to the starting position."""

        self.joint1_angle, self.joint2_angle, self.joint3_angle = self.START_JOINT1_ANGLE, self.START_JOINT2_ANGLE, self.START_JOINT3_ANGLE

        joint1_steps = calculations.steps_from_angle(self.START_JOINT1_ANGLE)
        joint2_steps = calculations.steps_from_angle(self.START_JOINT2_ANGLE)
        joint3_steps = calculations.steps_from_angle(self.START_JOINT3_ANGLE) - joint2_steps # na tomto sme stravili 4 dni!!!
        
        communication.send(self.serial, "coords", f"{joint1_steps},{joint2_steps},{joint3_steps}", output=self.OUTPUT)

    def tool(self, pw8: int = 0, pw9: int = 0, pw10: int = 0) -> None:
        """
        Sets the state of the tool (e.g., gripper open/close, suction on/off).

        Args:
            state: Dictionary with tool names as keys and desired states (True/False) as values.
        """
        communication.send(self.serial, "powers", f"{pw8},{pw9},{pw10}", output=self.OUTPUT)

    def get_angles(self) -> tuple[int, int, int]:
        """Returns the current base, upper, and lower arm angles."""
        return self.joint1_angle, self.joint2_angle, self.joint3_angle

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
