import cv2
from threading import Thread
import imgprocess as ip
#=========================================================
# a class that handles cameras
#=========================================================
class MyCamera(object):
    def __init__(self,port):
        self.port = port
        self.isThreading = False
        self.stream = cv2.VideoCapture(port)
        _, self.frame = self.stream.read()
    def setPort(self,port):
        self.port = port
        self.stream = cv2.VideoCapture(port)
    def isConnected(self):
        if self.stream.isOpened():
            ret, frame = self.stream.read()
            if ret > 0:
                return True
        else:
            return False
    #=========================================================
    # I/O in a thread
    #=========================================================
    def startThread(self):
        self.isThreading = True
        Thread(target=self.update, args=(), daemon=True).start()
    def stopThread(self):
        self.isThreading = False
    def update(self):
        while True:
            if not self.isThreading:
                cv2.destroyAllWindows()
                return
            _, self.frame = self.stream.read()
            cv2.imshow('Camera Port[{}]'.format(self.port), self.frame)
            key = cv2.waitKey(1) & 0xFF
