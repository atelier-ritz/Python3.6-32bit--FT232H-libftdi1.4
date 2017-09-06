


import time
import Adafruit_GPIO.FT232H as FT232H

# Temporarily disable FTDI serial drivers.
FT232H.use_FT232H()

# Find the first FT232H device.
ft232h = FT232H.FT232H()

# Create an I2C device at address 0x60.
i2c = FT232H.I2CDevice(ft232h, 0x60)

# Read a 16 bit unsigned little endian value from register 0x01.
# response = i2c.readU16(0x01)

# Write a 8 bit value 0xAB to register 0x02.
i2c.writeList(0x10, [0xFF,0xFF])
time.sleep(2)
# i2c.write8(0x01, 0xFF)
# time.sleep(2)
# i2c.write8(0x02, 0xFF)
# time.sleep(2)
# i2c.write8(0x03, 0xFF)
# time.sleep(2)
# i2c.write8(0x04, 0xFF)
# time.sleep(2)
# i2c.write8(0x05, 0xFF)
# time.sleep(2)
# i2c.write8(0x06, 0xFF)
# time.sleep(2)
# i2c.write8(0x07, 0xFF)
# time.sleep(2)
# i2c.write8(0x08, 0xFF)
# time.sleep(2)
# i2c.write8(0x09, 0xFF)
# time.sleep(2)
# i2c.write8(0x0a, 0xFF)
# time.sleep(2)
# i2c.write8(0x0b, 0xFF)
# time.sleep(2)
# i2c.write8(0x0c, 0xFF)
# time.sleep(2)
# i2c.write8(0x0d, 0xFF)
# time.sleep(2)
# i2c.write8(0x0e, 0xFF)
# time.sleep(2)
# i2c.write8(0x0f, 0xFF)
# time.sleep(2)
#
# i2c.write8(0x10, 0xFF)
# time.sleep(2)
# i2c.write8(0x11, 0xFF)
# time.sleep(2)
#
#
#
#
#






class MCP4728 :
  i2c = None

  # Registers
  __REG_WRITEDAC         = 0x40
  __REG_WRITEDACEEPROM   = 0x60

  # Constructor
  def __init__(self, address=0x62, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

  def setVoltage(self, voltage, persist=False):
    "Sets the output voltage to the specified value"
    if (voltage > 4095):
      voltage = 4095
    if (voltage < 0):
      voltage = 0
    if (self.debug):
      print("Setting voltage to {}".fotrmat(voltage))
    # Value needs to be left-shifted four bytes for the MCP4725
    bytes = [(voltage >> 4) & 0xFF, (voltage << 4) & 0xFF]
    if (persist):
      self.i2c.writeList(self.__REG_WRITEDACEEPROM, bytes)
    else:
      self.i2c.writeList(self.__REG_WRITEDAC, bytes)
