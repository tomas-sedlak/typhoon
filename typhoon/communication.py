import time
from typhoon.bcolors import bcolors

def send(serial, *lines, output = False):
    # Poslat data do typhoonu
    for line in lines:
        data = (line + "\n").encode()
        serial.write(data)

    # Arduino output
    while True:
        while serial.in_waiting > 0:
            response = serial.readline().decode().strip()

            if response == "Done":
                if output: print("-" * 50)
                return
            elif output:
                print(f"{bcolors.BOLD}>>{bcolors.ENDC} {response}")
        time.sleep(0.1)
