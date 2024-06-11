import typhoon, time

typhoon = typhoon.Typhoon("COM3", 130, 0, 0, output=True)

typhoon.move_to(100, 0, 0)
typhoon.move_to(0, 0, 0)

typhoon.close()