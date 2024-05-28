import typhoon

typhoon = typhoon.Typhoon(port="COM10", output=True)

typhoon.send_file("data.txt", ",")

# typhoon.send(0, 0, 0, sleep=2)

# typhoon.send(0, 0, 0, pw10=255, sleep=2)

# typhoon.send(0, 0, 0, sleep=2)

# typhoon.send(0, 0, 0, pw10=255, sleep=2)

# typhoon.send(0, 0, 0)

typhoon.close()