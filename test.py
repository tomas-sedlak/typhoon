import typhoon

typhoon = typhoon.Typhoon(port="COM10")

for i in range(4):
    for j in range(4):
        typhoon.send(i * 80, j * 80, i * 20)

typhoon.send(0, 0, 0)

typhoon.close()