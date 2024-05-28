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
import math
import struct
import time

try:
    import serial
except ImportError:
    print("[ERROR] Nemas nainstalovanu kniznicu pyserial.")
    print("[ERROR] Nainstalujes ju pomocou: pip install pyserial")
    sys.exit(0)


class Typhoon():
    def __init__(self, port: str, length_upper_arm: int = 215, length_lower_arm: int = 250, distance_tool: int = 165, distance_z: int = 0, height_from_ground: int = 0, output: bool = False):
        try:
            self.arduino_serial = serial.Serial(port, 115200)
            self.arduino_serial.flushInput()
            time.sleep(1.5)
        except serial.serialutil.SerialException:
            print(f"[ERROR] Neda sa otvorit port '{port}'.")
            print("[ERROR] Skus nejaky iny port alebo pozri ci mas zapojeny kabel.")
            sys.exit(0)

        self.OUTPUT = output
        self.LENGTH_UPPER_ARM = length_upper_arm
        self.LENGTH_LOWER_ARM = length_lower_arm
        self.DISTANCE_TOOL = distance_tool
        self.DISTANCE_Z = distance_z
        self.HEIGTH_FROM_GROUND = height_from_ground
        self.LENGTH_REAR_SQUARED = pow(self.LENGTH_UPPER_ARM, 2)
        self.LENGTH_FRONT_SQUARED = pow(self.LENGTH_LOWER_ARM, 2)
        self.PI_HALF = math.pi / 2

        print("[SUCCESS] Uspesne pripojene!")

    def angles_from_coordinates(self, x: int, y: int, z: int):
        x += self.DISTANCE_TOOL
        z += self.DISTANCE_Z
        radius = math.sqrt(pow(x, 2) + pow(y*0.5, 2))

        base_angle = math.atan2(y*0.5, x)
        actual_z = z - self.HEIGTH_FROM_GROUND
        hypotenuse_squared = pow(actual_z, 2) + pow(radius, 2)
        hypotenuse = math.sqrt(hypotenuse_squared)

        q1 = math.atan2(actual_z, radius)
        q2 = math.acos((self.LENGTH_REAR_SQUARED - self.LENGTH_FRONT_SQUARED +
                       hypotenuse_squared) / (2 * self.LENGTH_UPPER_ARM * hypotenuse))

        rear_angle = self.PI_HALF - (q1 + q2)
        front_angle = self.PI_HALF - (math.acos((self.LENGTH_REAR_SQUARED + self.LENGTH_FRONT_SQUARED -
                                                 hypotenuse_squared) / (2 * self.LENGTH_UPPER_ARM * self.LENGTH_LOWER_ARM)) - rear_angle)

        # return base_angle * 180 / math.pi, -rear_angle * 180 / math.pi + 67.9130669909833, 77.87547181797633 - front_angle * 180 / math.pi
        return math.degrees(base_angle), math.degrees(-rear_angle) + 9.120851906137954, 61.64548899867737 - math.degrees(front_angle)

    def send(self, x: int, y: int, z: int, pw8: int = 0, pw9: int = 0, pw10: int = 0):
        base_angle, upper_angle, lover_angle = self.angles_from_coordinates(x, y, z)

        # Poslat data do typhoonu
        self.arduino_serial.write(struct.pack("f", base_angle))
        self.arduino_serial.write(struct.pack("f", lover_angle))
        self.arduino_serial.write(struct.pack("f", upper_angle))
        # hodnota pre nastroj v D8
        self.arduino_serial.write(struct.pack("f", pw8))
        # hodnota pre nastroj v D9
        self.arduino_serial.write(struct.pack("f", pw9))
        # hodnota pre nastroj v D10
        self.arduino_serial.write(struct.pack("f", pw10))

        # for _ in range(0, 4):  # podla poctu Serial.println v firmware-arduino
        #     self.arduino_serial.readline()
        #     if self.OUTPUT:
        #         print(">>", self.arduino_serial.readline().strip().decode("utf-8"))

    def send_file(self, file_path: str):
        _file = open(file_path, "r")

        for line in _file:
            line = line.strip().split()
            x = float(line[0])
            y = float(line[1])
            z = float(line[2])
            pw8 = float(line[3])  # 0 ... 255
            pw9 = float(line[4])  # 0 ... 255
            pw10 = float(line[5])  # 0 ... 255

            self.send(x, y, z, pw8, pw9, pw10)
