import Adafruit_GPIO.FT232H as FT232H

import atexit

class MCP4728(FT232H.I2CDevice):
    # Registers
    """ Refer to MCP4728 datasheet [5.5 Writing and Reading Registers
    and EEPROM] for more information"""
    __REG_EEPROM_CH_A = 0x58
    __REG_EEPROM_CH_B = 0x5A
    __REG_EEPROM_CH_C = 0x5C
    __REG_EEPROM_CH_D = 0x5E

    CHANNEL = {
                0:__REG_EEPROM_CH_A,
                1:__REG_EEPROM_CH_B,
                2:__REG_EEPROM_CH_C,
                3:__REG_EEPROM_CH_D
            }

    def __init__(self, ft232h, address=0x60, clock_hz=400000):
        super().__init__(ft232h,address,clock_hz)
        self.writeRaw8(0x8F) # use reference voltage 2.048V for all channels
        self.clearVoltage()
        # clear voltage output at normal exit (not executed when unexpected error happens)
        atexit.register(self.clearVoltage)

    def setVoltage(self, channel, voltage):
    # """This command writes to a single selected DAC input register and its
    # EEPROM. Both the input register and EEPROM are written at the
    # acknowledge clock pulse of the last input data byte."""
        if (voltage > 4095):
            voltage = 4095
        if (voltage < 0):
            voltage = 0
        voltage = voltage & 0x0FFF | 0x9000
        self.write16(self.CHANNEL[channel],voltage,little_endian=False)

    def clearVoltage(self):
        self.write16(self.__REG_EEPROM_CH_A,0x0000)
        self.write16(self.__REG_EEPROM_CH_B,0x0000)
        self.write16(self.__REG_EEPROM_CH_C,0x0000)
        self.write16(self.__REG_EEPROM_CH_D,0x0000)
