import typhoon, time

poz_d_x, poz_d_y = 100, 98
zobrat_0_x, zobrat_0_y = 20, 95
zobrat_1_x, zobrat_1_y = 60, 95
zdvih = 50

robot = typhoon.Typhoon("COM13") # toto zmen ak ti program nefunguje

def move(robot, binary_num):
    binary_num = binary_num[::-1]
    start_x, start_y = poz_d_x, poz_d_y
    zero_x, zero_y = zobrat_0_x, zobrat_0_y
    one_x, one_y = zobrat_1_x, zobrat_1_y

    robot.send_x_y_z_pw(0, 0, zdvih, 0)  # zaciatocna pozicia

    for digit in binary_num:
        if digit == "0":
            grab(zero_x, zero_y)
            zero_y -= 30
        elif digit == "1":
            grab(one_x, one_y)
            one_y -= 30
        
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

    for digit in binary_num:
        grab(start_x, start_y)
        start_y -= 30

        if digit == "0":
            place(zero_x, zero_y)
            zero_y -= 30
        elif digit == "1":
            place(one_x, one_y)
            one_y -= 30

    # konecna pozicia
    robot.send_x_y_z_pw(0, 0, zdvih, 0)
    robot.send_x_y_z_pw(0, 0, 0, 0)

def grab(x, y):
    robot.send_x_y_z_pw(x, y, zdvih, 0)
    robot.send_x_y_z_pw(x, y, 0, 0)
    robot.send_x_y_z_pw(x, y, 0, 255)
    robot.send_x_y_z_pw(x, y, zdvih, 255)

def place(x, y):
    robot.send_x_y_z_pw(x, y, zdvih, 255)
    robot.send_x_y_z_pw(x, y, 0, 255)
    robot.send_x_y_z_pw(x, y, 0, 0)
    robot.send_x_y_z_pw(x, y, zdvih, 0)

while True:
    decimal_num = int(input("Cislo v desiatkovej sustave: "))
    binary_num = bin(decimal_num)[2:]
    
    print(binary_num, "v dvojkovej sustave je", decimal_num)
    move(robot, binary_num)

    time.sleep(2)

    print("Upratujem...")
    clean(robot, binary_num)