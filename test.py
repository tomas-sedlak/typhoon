import typhoon

typhoon = typhoon.Typhoon("COM10", 135, 0, 0, 50, 0, 75)

typhoon.send_coords(100, 0, 0)
typhoon.send_coords(0, 0, 0)

typhoon.close()