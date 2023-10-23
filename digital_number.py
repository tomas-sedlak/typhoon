import typhoon

robot = typhoon.Typhoon("COM13")

number = int(input("Cislo v desiatkovej sustave: "))
digit = bin(number).replace("0b", "")
print(number, "v dvojkovej sustave je", digit)
digit = digit[::-1]

poz_d_x, poz_d_y = 100, 98
zobrat_0_x, zobrat_0_y = 20, 95
zobrat_1_x, zobrat_1_y = 60, 95
zdvih = 50

robot.send_x_y_z_pw(0, 0, zdvih, 0)  # zaciatocna pozicia

for d in digit:
    if d == "0":
        robot.send_x_y_z_pw(zobrat_0_x, zobrat_0_y, zdvih, 0)
        robot.send_x_y_z_pw(zobrat_0_x, zobrat_0_y, 0, 255)
        robot.send_x_y_z_pw(zobrat_0_x, zobrat_0_y, zdvih, 255)

        print(d, 'z pozicie x:', zobrat_0_x, 'y:', zobrat_0_y)
        zobrat_0_y -= 30

    elif d == "1":
        robot.send_x_y_z_pw(zobrat_1_x, zobrat_1_y, zdvih, 0)
        robot.send_x_y_z_pw(zobrat_1_x, zobrat_1_y, 0, 255)
        robot.send_x_y_z_pw(zobrat_1_x, zobrat_1_y, zdvih, 255)

        print(d, 'z pozicie x:', zobrat_1_x, 'y:', zobrat_1_y)
        zobrat_1_y -= 30
    
    robot.send_x_y_z_pw(poz_d_x, poz_d_y, zdvih, 255)
    robot.send_x_y_z_pw(poz_d_x, poz_d_y, 0, 255)
    robot.send_x_y_z_pw(poz_d_x, poz_d_y, 0, 0)
    robot.send_x_y_z_pw(poz_d_x, poz_d_y, zdvih, 0)

    print(' umiestnit na x:', poz_d_x, 'y:', poz_d_y)
    poz_d_y -= 30

# konecna pozicia
robot.send_x_y_z_pw(0, 0, zdvih, 0)
robot.send_x_y_z_pw(0, 0, 0, 0)