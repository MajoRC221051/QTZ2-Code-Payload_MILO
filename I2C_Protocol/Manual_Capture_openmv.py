import sensor
import image
import time
import os
from pyb import UART
from machine import reset

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

# --------- UART ---------
uart = UART(3, 115200, timeout_char=1000)

photo_counter = 0

print("System ready, waiting for command")


while(True):

    if uart.any():
        cmd = uart.readline()

        if cmd is not None:
            cmd = cmd.decode().strip()

            if cmd == "TAKE":
                img = sensor.snapshot()
                filename = "/photo_%d.jpg" % photo_counter
                img.save(filename)
                uart.write("OK\n")
                photo_counter += 1

            elif cmd == "DELETE":
                for file in os.listdir():
                    if file.endswith(".jpg"):
                        os.remove(file)
                uart.write("DELETED\n")

            elif cmd == "RESET":
                uart.write("RESETTING\n")
                time.sleep_ms(100)
                reset()

            else:
                uart.write("UNKNOWN\n")
