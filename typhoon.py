print(
'''
  _______          _
 |__   __|        | |
    | |_   _ _ __ | |__   ___   ___  _ __
    | | | | | '_ \| '_ \ / _ \ / _ \| '_ \\
    | | |_| | |_) | | | | (_) | (_) | | | |
    |_|\__, | .__/|_| |_|\___/ \___/|_| |_|
        __/ | |
       |___/|_|
''')

import sys
import time
from math import sqrt, atan2, acos, sin, cos, degrees, pi

try:
    import serial
except ImportError:
    print("[ERROR] Nemas nainstalovanu kniznicu pyserial.")
    print("[ERROR] Nainstalujes ju pomocou: pip install pyserial")
    sys.exit(0)


class Typhoon():
    def __init__(self, port: str, start_x: int, start_y: int, start_z: int, tool_x: int = 0, tool_y: int = 0, tool_z: int = 0, output: bool = False, length_upper_arm: int = 215, length_lower_arm: int = 250):
        try:
            self.arduino_serial = serial.Serial(port, 115200)
            self.arduino_serial.flushInput()
            time.sleep(1.5)
        except serial.serialutil.SerialException:
            print(f"[ERROR] Neda sa otvorit port '{port}'.")
            print("[ERROR] Skus nejaky iny port alebo pozri ci mas zapojeny kabel.")
            sys.exit(0)

        self.START_X = start_x
        self.START_Y = start_y
        self.START_Z = start_z
        self.TOOL_X = tool_x
        self.TOOL_Y = tool_y
        self.TOOL_Z = tool_z
        self.OUTPUT = output
        self.LENGTH_UPPER_ARM = length_upper_arm
        self.LENGTH_LOWER_ARM = length_lower_arm
        # self.LENGTH_REAR_SQUARED = pow(self.LENGTH_UPPER_ARM, 2)
        # self.LENGTH_FRONT_SQUARED = pow(self.LENGTH_LOWER_ARM, 2)
        # self.PI_HALF = math.pi / 2

        print(f"[SUCCESS] Uspesne pripojene cez port '{port}'!")

    def angles_from_coords(self, x: int, y: int, z: int):
        x += self.START_X
        # y += self.START_Y

        print(x, y, z)

        r = sqrt(x**2 + y**2)
        q1 = atan2(y, x)
        q3 = acos((r**2 + z**2 - self.LENGTH_UPPER_ARM**2 - self.LENGTH_LOWER_ARM**2) / (2 * self.LENGTH_UPPER_ARM * self.LENGTH_LOWER_ARM))
        q2 = atan2(z, r) + atan2(self.LENGTH_LOWER_ARM * sin(q3), self.LENGTH_UPPER_ARM + self.LENGTH_LOWER_ARM * cos(q3))

        # actual_z = z - self.HEIGTH_FROM_GROUND + radius/6.2
        # hypotenuse_squared = pow(actual_z, 2) + pow(radius, 2)
        # hypotenuse = math.sqrt(hypotenuse_squared)

        # q1 = math.atan2(actual_z, radius)
        # q2 = math.acos((self.LENGTH_REAR_SQUARED - self.LENGTH_FRONT_SQUARED +
        #                hypotenuse_squared) / (2 * self.LENGTH_UPPER_ARM * hypotenuse))

        # rear_angle = self.PI_HALF - (q1 + q2)
        # front_angle = self.PI_HALF - (math.acos((self.LENGTH_REAR_SQUARED + self.LENGTH_FRONT_SQUARED -
        #                                          hypotenuse_squared) / (2 * self.LENGTH_UPPER_ARM * self.LENGTH_LOWER_ARM)) - rear_angle)

        # return base_angle * 180 / math.pi, -rear_angle * 180 / math.pi + 67.9130669909833, 77.87547181797633 - front_angle * 180 / math.pi
        # return math.degrees(base_angle), math.degrees(-rear_angle)+1.3, 40.5- math.degrees(front_angle)

        print(degrees(q1), degrees(pi / 2 - q2), degrees(q3))

        return degrees(q1), degrees(pi / 2 - q2), degrees(-1 * (q3 - q2))

    def send_coords(self, x: int, y: int, z: int):
        base_angle, upper_angle, lower_angle = self.angles_from_coords(x, y, z)
        print(base_angle, upper_angle, lower_angle)

        # Poslat data do typhoonu
        data = f"{base_angle},{lower_angle},{upper_angle}\n".encode()
        self.arduino_serial.write("coords\n".encode())
        self.arduino_serial.write(data)

        # Arduino output
        while True:
            while self.arduino_serial.in_waiting > 0:
                response = self.arduino_serial.readline().decode().strip()
                if response == "Done":
                    return
                elif self.OUTPUT:
                    print(">>", response)
            time.sleep(0.1)
    
    def send_powers(self, pw8: int = 0, pw9: int = 0, pw10: int = 0):
        # Poslat data do typhoonu
        data = f"{pw8},{pw9},{pw10}\n".encode()
        self.arduino_serial.write("powers\n".encode())
        self.arduino_serial.write(data)

        # Arduino output
        while True:
            while self.arduino_serial.in_waiting > 0:
                response = self.arduino_serial.readline().decode().strip()
                if response == "Done":
                    return
                elif self.OUTPUT:
                    print(">>", response)
            time.sleep(0.1)

    def send_file(self, file_path: str, separator: str = " "):
        _file = open(file_path, "r")

        for line in _file:
            items = line.strip().split(separator)
            float_items = [float(item) for item in items]
            self.send(*float_items)

    def close(self):
        self.arduino_serial.close()
