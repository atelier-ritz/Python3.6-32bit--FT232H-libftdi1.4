from PyQt5 import QtCore, QtWidgets, uic
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H
from MCP4728 import MCP4728
from random import randint

# UI config
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# ft232h config
FT232H.use_FT232H()
ft232h = FT232H.FT232H()

# GPIO config
ft232h.setup(7, GPIO.IN)   # Make pin D7 a digital input.
ft232h.setup(8, GPIO.IN)  # Make pin C0 a digital input.

# MCP4728 (DAC) config
i2c = MCP4728(ft232h, address=0x60, clock_hz=400000)

class GUI(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # Since slider and spinbox are connected in Qt designer,
        # you only need to bind the function to one of them
        self.sld_voltA.valueChanged.connect(self.on_sld_voltA)
        self.sld_voltB.valueChanged.connect(self.on_sld_voltB)
        self.sld_voltC.valueChanged.connect(self.on_sld_voltC)
        self.sld_voltD.valueChanged.connect(self.on_sld_voltD)

        # Fuction "update" is executed every 100 msec
        self.my_timer = QtCore.QTimer()
        self.my_timer.timeout.connect(self.update)
        self.my_timer.start(100) # msec

        self.my_timer2 = QtCore.QTimer()
        self.my_timer2.timeout.connect(self.update2)
        self.my_timer2.start(10) # msec
        self.c = 0

    def on_sld_voltA(self,val):
        i2c.setVoltage(0,val)
    def on_sld_voltB(self,val):
        i2c.setVoltage(1,val)
    def on_sld_voltC(self,val):
        i2c.setVoltage(2,val)
    def on_sld_voltD(self,val):
        i2c.setVoltage(3,val)

    def update(self):
        level7 = ft232h.input(7)
        level8 = ft232h.input(8)
        if level7 == GPIO.LOW:
            self.lbl_d7.setNum(0)
        else:
            self.lbl_d7.setNum(1)
        if level8 == GPIO.LOW:
            self.lbl_c0.setNum(0)
        else:
            self.lbl_c0.setNum(1)

    def update2(self):
        self.c += 8
        if self.c >= 4095:
            self.c = 0
        self.sld_voltB.setValue(self.c)
