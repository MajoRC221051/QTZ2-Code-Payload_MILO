# Capture with I2C and automatic reset Feb 25 2026

import sensor
from pyb import I2C
import machine

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.

i2c = I2C(2, I2C.SLAVE, addr=0x12)

capture_count = 0 

led = machine.LED("LED_BLUE")

while True:
    led.toggle()
    sensor.snapshot()
    try:
        data = i2c.recv(1, timeout=500) # Delay

        print("Dato recibido:", data)

        if data == b'\x55':
            capture_count+=1
            img = sensor.snapshot()
            print ("Captura #", capture_count)
            print ("Captura lista")
            led.off()
            img.save("example.jpg")
            #machine.reset()

    except OSError:
        pass
