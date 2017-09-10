import sys
from callbacks import GUI
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
