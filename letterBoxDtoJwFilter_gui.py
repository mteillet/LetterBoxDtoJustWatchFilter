# letterBoxDtoJwFilter_gui.py
from PyQt5 import QtWidgets, QtCore, QtGui
import sys


class MainWindow(QtWidgets.QWidget):
    '''
    Main UI part
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Letter Box D list to Just Watch Availability")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle("Fusion")

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())