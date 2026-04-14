# Test 1 - I2C communication and physical test - Feb 20 2026

from pyb import I2C
from pyb import LED

i2c = I2C(2, I2C.SLAVE, addr=0x12)
led = LED(1)

while True:
    try:
        data = i2c.recv(1)  # Espera 1 byte

        if data == b'\x10':
            led.on()

    except OSError:
        # No hay datos disponibles
        pass
