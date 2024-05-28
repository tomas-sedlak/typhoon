# Fonkcne, musi byt time.sleep(0.001)
import time, tkinter
import RPi.GPIO as GPIO

size, rect = 400, 400 / 8
canvas = tkinter.Canvas(width=size, height=size)
canvas.pack()

pole_st = []
for i in range(9):
    riadky = []
    for j in range(9):
        riadky.append(1)
        pole_st.append(riadky)
pole = []
for i in range(9):
    riadky = []
    for j in range(9):
        riadky.append(1)
    pole.append(riadky)


def draw():
    for row in range(8):
        for col in range(8):
            color = "yellow" if pole[row + 1][col + 1] else "red"
            canvas.create_rectangle(rect * col, rect * row, rect * (col + 1), rect * (row + 1), fill=color)


def tah():
    global pole
    r, s = [0] * 10, [0] * 10
    s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8] = 17, 27, 22, 5, 6, 13, 19, 26
    r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8] = 2, 3, 4, 25, 8, 7, 23, 24

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in range(1, 9): GPIO.setup(s[i], GPIO.IN)
    for i in range(1, 9): GPIO.setup(r[i], GPIO.OUT)
    # Ak je na sachovnici figurka pole[cr][cs]=1 a naopak. Vyhodnotenie pomocou fototranzistora.
    # Ak nie je nad fototranzistorom figurka, fototranzistor vedie prud: - if GPIO.input(s[cs])==1:pole[cr][cs]=0                                                                              # - else:pole[cr][cs]=1

    for cr in range(1, 9):
        GPIO.output(r[cr], 1)
        time.sleep(0.005)
        for cs in range(1, 9):
            inpu = GPIO.input(s[cs])

            if inpu == 1:
                pole[cr][cs] = 0

            if inpu == 0:
                pole[cr][cs] = 1
        GPIO.output(r[cr], 0)
    GPIO.cleanup()
    return pole


while True:
    pole_st = tah()
    draw()
    canvas.update_idletasks()
    canvas.update()

