import Adafruit_GPIO.FT232H as FT232H
import time
# import Adafruit_GPIO as GPIO
# Temporarily disable FTDI serial drivers.
FT232H.use_FT232H()

# Find the first FT232H device.
ft232h = FT232H.FT232H()

# Create a SPI interface from the FT232H using pin 8 (C0) as chip select.
# Use a clock speed of 3mhz, SPI mode 0, and most significant bit first.
spi = FT232H.SPI(ft232h, cs=8, max_speed_hz=100000, mode=0, bitorder=FT232H.MSBFIRST)
i=0
# ft232h.setup(8,0)#out write
# ft232h.setup(8, GPIO.OUT)  # Make pin C0 a digital output.
while True:
# Write three bytes (0x01, 0x02, 0x03) out using the SPI protocol.
    i += 1
    if i > 255: i = 0
    spi.write([0x11, i])
    time.sleep(0.1)
    # ft232h.set_low(8)
    # time.sleep(0.1)
    # ft232h.set_high(8)
    # time.sleep(0.1)
