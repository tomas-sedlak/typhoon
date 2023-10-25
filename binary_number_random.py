import sys
import time
import random

try:
     from typhoon import Typhoon
except ImportError:
     print("[ERROR] Nenasiel sa modul Typhoon.")
     print("[ERROR] Najdes ho na GitHube: https://github.com/tomas-sedlak/typhoon")
     sys.exit(0)

poz_d_x, poz_d_y = 100, 98
zobrat_0_x, zobrat_0_y = 20, 95
zobrat_1_x, zobrat_1_y = 60, 95
zdvih = 50

robot = Typhoon("COM10") # toto zmen ak ti program nefunguje

def move(robot, binary_num):
    start_x, start_y = poz_d_x, poz_d_y
    zero_x, zero_y = zobrat_0_x, zobrat_0_y
    one_x, one_y = zobrat_1_x, zobrat_1_y

    robot.send_x_y_z_pw(0, 0, zdvih, 0)  # zaciatocna pozicia

    for i, digit in enumerate(binary_num):
        if digit == "0":
            print("Beriem cislo 0")
            grab(zero_x, zero_y - (i * 30))
        elif digit == "1":
            print("Beriem cislo 1")
            grab(one_x, one_y - (i * 30))
        
        place(start_x, start_y)
        start_y -= 30

    # konecna pozicia
    robot.send_x_y_z_pw(0, 0, zdvih, 0)
    robot.send_x_y_z_pw(0, 0, 0, 0)

def clean(robot, binary_num):
    start_x, start_y = poz_d_x, poz_d_y
    zero_x, zero_y = zobrat_0_x, zobrat_0_y
    one_x, one_y = zobrat_1_x, zobrat_1_y

    robot.send_x_y_z_pw(0, 0, zdvih, 0)  # zaciatocna pozicia

    for i, digit in enumerate(binary_num):
        grab(start_x, start_y)
        start_y -= 30

        if digit == "0":
            print("Upratujem cislo 0")
            place(zero_x, zero_y - (i * 30))
        elif digit == "1":
            print("Upratujem cislo 1")
            place(one_x, one_y - (i * 30))

    # konecna pozicia
    robot.send_x_y_z_pw(0, 0, zdvih, 0)
    robot.send_x_y_z_pw(0, 0, 0, 0)

def grab(x, y):
    robot.send_x_y_z_pw(x, y, zdvih, 0)
    robot.send_x_y_z_pw(x, y, 0, 0)
    robot.send_x_y_z_pw(x, y, 0, 255)
    time.sleep(0.25)
    robot.send_x_y_z_pw(x, y, zdvih, 255)

def place(x, y):
    robot.send_x_y_z_pw(x, y, zdvih, 255)
    robot.send_x_y_z_pw(x, y, 0, 255)
    robot.send_x_y_z_pw(x, y, 0, 0)
    time.sleep(0.25)
    robot.send_x_y_z_pw(x, y, zdvih, 0)

while True:
    decimal_num = random.randrange(256)
    binary_num = bin(decimal_num)[2:]
    print(binary_num, "v dvojkovej sustave je", decimal_num)
    
    move(robot, binary_num)

    time.sleep(10)

    print("Upratujem...")
    clean(robot, binary_num)
    print("Hotovo!")

    time.sleep(10)