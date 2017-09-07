import Adafruit_GPIO.FT232H as FT232H
import math
import time
import atexit
import threading

class MCP4728(FT232H.I2CDevice):
    # [Registers] Refer to MCP4728 datasheet [5.5 Writing and Reading Registers and EEPROM] for more information
    # EEPROM: nonvolatile memory feature enables the DAC device to hold the DAC input codes during power-off time
    __REG_EEPROM_CH_A = 0x58
    __REG_EEPROM_CH_B = 0x5A
    __REG_EEPROM_CH_C = 0x5C
    __REG_EEPROM_CH_D = 0x5E
    # Input register: loses data when powered off
    __REG_CH_A = 0x40
    __REG_CH_B = 0x42
    __REG_CH_C = 0x44
    __REG_CH_D = 0x46

    CHANNEL_EEPROM = [__REG_EEPROM_CH_A, __REG_EEPROM_CH_B, __REG_EEPROM_CH_C, __REG_EEPROM_CH_D]
    CHANNEL_DIRECT = [__REG_CH_A, __REG_CH_B, __REG_CH_C, __REG_CH_D]

    def __init__(self, ft232h, address=0x60, clock_hz=400000):
        super().__init__(ft232h,address,clock_hz)
        self.clearEEPROM()
        atexit.register(self.clearEEPROM) # clear voltage output at normal exit (not executed when unexpected error happens)

    def setVoltage(self, channel, voltage, eeprom=False, internal_refvdd=True):
        if (voltage > 4095):
            voltage = 4095
        if (voltage < 0):
            voltage = 0
        voltage = voltage & 0x0FFF
        if internal_refvdd:
            voltage = voltage | 0x9000 # by default gain = 2 when using refvdd = 2.048V, swith to gain = 1 by 0x8000
        if eeprom:
            self.write16(self.CHANNEL_EEPROM[channel], voltage, little_endian=False)
        else:
            self.write16(self.CHANNEL_DIRECT[channel], voltage, little_endian=False)

    def clearEEPROM(self):
        for register in self.CHANNEL_EEPROM:
            self.write16(register ,0x0000)
