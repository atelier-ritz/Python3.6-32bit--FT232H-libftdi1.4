from PyQt5 import QtCore, QtWidgets, uic
import Adafruit_GPIO.FT232H as FT232H
from MCP4728 import MCP4728
from camera import MyCamera
import math
import time
import cv2
import ctypes

#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================
# UI config
qtCreatorFile = "mainwindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
# ft232h config
FT232H.use_FT232H()
ft232h = FT232H.FT232H()
# MCP4728 (DAC) config
i2c = MCP4728(ft232h, address=0x60, clock_hz=450000)
# cameras config
cam1 = MyCamera(0)
cam2 = MyCamera(1)

#=========================================================
# a class that handles the signal and callbacks of the GUI
#=========================================================
class GUI(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        #========================================================
        # signals and handlers
        #========================================================
        self.sld_voltA.valueChanged.connect(self.on_sld_voltA)
        self.sld_voltB.valueChanged.connect(self.on_sld_voltB)
        self.sld_voltC.valueChanged.connect(self.on_sld_voltC)
        self.sld_voltD.valueChanged.connect(self.on_sld_voltD)
        self.chb_generateA.toggled.connect(self.on_chb_generateA)
        #========================================================
        self.btn_initcam1.clicked.connect(self.on_btn_initcam1)
        self.btn_initcam2.clicked.connect(self.on_btn_initcam2)
        self.chb_showcam1.toggled.connect(self.on_chb_showcam1)
        self.chb_showcam2.toggled.connect(self.on_chb_showcam2)
        #========================================================
        # timer object
        #========================================================
        self.siggen_timer = QtCore.QTimer()
        self.siggen_timer.timeout.connect(self.tmr_updateSiggen)
        self.siggenCounter = 0

    #========================================================
    # GUI callbacks
    #========================================================
    def on_sld_voltA(self,val):
        i2c.setVoltage(0,val)
    def on_sld_voltB(self,val):
        i2c.setVoltage(1,val)
    def on_sld_voltC(self,val):
        i2c.setVoltage(2,val)
    def on_sld_voltD(self,val):
        i2c.setVoltage(3,val)
    def on_chb_generateA(self,boolean):
        if boolean:
            self.siggen_timer.start(self._getTimerInterval())
        else:
            self.siggen_timer.stop()
    #========================================================
    def on_btn_initcam1(self):
        if self.chb_showcam1.isChecked():
            errortitle = u'Failed to initialize'
            errormsg = u'Please uncheck <Show cam1> checkbox!'
            ctypes.windll.user32.MessageBoxW(None, errormsg, errortitle, 0)
        else:
            port = self.spb_portcam1.value()
            cam1.setPort(port)
            if cam1.isConnected():
                self.lab_statecam1.setText('Connected')
                self.chb_showcam1.setEnabled(True)
            else:
                self.lab_statecam1.setText('Disconnected')
                self.chb_showcam1.setEnabled(False)
    def on_btn_initcam2(self):
        if self.chb_showcam2.isChecked():
            errortitle = u'Failed to initialize'
            errormsg = u'Please uncheck <Show cam2> checkbox!'
            ctypes.windll.user32.MessageBoxW(None, errormsg, errortitle, 0)
        else:
            port = self.spb_portcam2.value()
            cam2.setPort(port)
            if cam2.isConnected():
                self.lab_statecam2.setText('Connected')
                self.chb_showcam2.setEnabled(True)
            else:
                self.lab_statecam2.setText('Disconnected')
                self.chb_showcam2.setEnabled(False)
    def on_chb_showcam1(self,boolean):
        if boolean:
            cam1.startThread()
        else:
            cam1.stopThread()
    def on_chb_showcam2(self,boolean):
        if boolean:
            cam2.startThread()
        else:
            cam2.stopThread()

    #========================================================
    # timer functions
    #========================================================
    def tmr_updateSiggen(self):
        samplerate, freq, amp, offset = self._getSiggenParam()
        self.siggen_timer.start(self._getTimerInterval())
        self._siggenCounterInc()
        val = int(math.sin(2*math.pi * self.siggenCounter/(samplerate+1)) * amp + offset)
        i2c.setVoltage(0,val)

    #========================================================
    # private functions
    #========================================================
    def _getSiggenParam(self):
        samplerate = self.spb_samplerate.value()
        freq = self.dspb_freqA.value()
        amp = self.spb_ampA.value()
        offset = self.spb_offsetA.value()
        return (samplerate,freq,amp,offset)
    def _getTimerInterval(self):
        samplerate, freq, _, _ = self._getSiggenParam()
        if freq > 0:
            updateRate = (1/freq) / samplerate * 1000
            return updateRate # miliseconds
        else:
            print('Frequency must be positive! Timer interval is set to 1000 ms.')
            return 1000
    def _siggenCounterInc(self):
        samplerate, _, _, _ = self._getSiggenParam()
        self.siggenCounter += 1
        if self.siggenCounter >= samplerate:
            self.siggenCounter = 0
