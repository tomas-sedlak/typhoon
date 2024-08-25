import time
from serial import Serial
from typhoon.utils import bcolors

class Communication:
    def send(self, serial: Serial, *lines, output = False) -> None:
        """
        Sends data to the Typhoon and optionally prints the response.

        Args:
            serial: The serial object representing the Typhoon.
            lines: Data that should be sent to Typhoon.
            output: Whether to print the received response (default: False).
        """

        # Send data to typhoonu
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
