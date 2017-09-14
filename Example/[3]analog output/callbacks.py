from PyQt5 import QtCore, QtWidgets, uic
import Adafruit_GPIO.FT232H as FT232H
from MCP4728 import MCP4728
import math
import time

# UI config
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# ft232h config
FT232H.use_FT232H()
ft232h = FT232H.FT232H()

# MCP4728 (DAC) config
i2c = MCP4728(ft232h, address=0x60, clock_hz=450000)

class GUI(QtWidgets.QMainWindow,Ui_MainWindow):

    SIGGEN_SAMPLE_RATE = 16 # sample 16 points in each period, can be 2, 4, 8, 16, 32, etc.

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.sld_voltA.valueChanged.connect(self.on_sld_voltA)
        self.sld_voltB.valueChanged.connect(self.on_sld_voltB)
        self.sld_voltC.valueChanged.connect(self.on_sld_voltC)
        self.sld_voltD.valueChanged.connect(self.on_sld_voltD)
        self.chb_generateA.toggled.connect(self.on_chb_generateA)

        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.updateSignalGenerator)
        self.siggenCounter = 0

    def on_sld_voltA(self,val):
        i2c.setVoltage(0,val)
    def on_sld_voltB(self,val):
        i2c.setVoltage(1,val)
    def on_sld_voltC(self,val):
        i2c.setVoltage(2,val)
    def on_sld_voltD(self,val):
        i2c.setVoltage(3,val)
    def on_chb_generateA(self,boolean):
        if boolean == True:
            freq = self.dspb_freqA.value()
            updateRate = (1 / freq) / (self.SINWAVE_SAMPLE_RATE) # sec
            self.my_timer.start(updateRate*1000) # msec
        else:
            self.my_timer.stop()

    def updateSignalGenerator(self):
        waveform = self.cbb_waveformA.currentIndex()
        amp = self.spb_ampA.value()
        offset = self.spb_offsetA.value()
        freq = self.dspb_freqA.value()
        samplerate = self.SIGGEN_SAMPLE_RATE
        if not freq == 0:
            updateRate = (1 / freq) / (self.SINWAVE_SAMPLE_RATE) # sec
            self.my_timer.start(updateRate*1000)
        if waveform == 1:    # sin
            self.siggenCounter += 1
            if self.siggenCounter >= samplerate:
                self.siggenCounter = 0
            val = int(math.sin(2 * math.pi * self.siggenCounter / (samplerate + 1))*amp+offset)
            i2c.setVoltage(0,val)
        if waveform == 2:   # square
            self.siggenCounter += samplerate / 2
            if self.siggenCounter >= samplerate:
                self.siggenCounter = 0
            val = int((-1) ** self.siggenCounter / (samplerate + 1))*amp+offset)
            i2c.setVoltage(0,val)
        if waveform == 3:   # triangle
            #i2c.setVoltage(0,val)
