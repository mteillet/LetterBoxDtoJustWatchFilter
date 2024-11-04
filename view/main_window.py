# main_window.py

from PySide2 import QtWidgets, QtCore, QtGui

class Main_Window(QtWidgets.QWidget):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setWindowTitle("LetterBoxD JustWatch Filter")
        self.build_gui()

    def build_gui(self):
        """
        Call this function to begin building the base UI
        """
        ##############
        #   WIDGETS  #
        ##############
        self.label = QtWidgets.QLabel("Label")

        ##############
        #   LAYOUT   #
        ##############
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

