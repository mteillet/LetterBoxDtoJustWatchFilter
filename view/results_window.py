# results_window.py
from PySide2 import QtWidgets, QtCore, QtGui

class ResultsWindow(QtWidgets.QWidget):
    """
    Class for displaying the film results 
    """
    def __init__(self):
        super(ResultsWindow, self).__init__()
        self.setWindowTitle("Scan Results")
        self.resize(1280, 720)
        self.build_gui()

    def build_gui(self):
        """
        Init the widgets and layouts to build the gui
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.tmp_lbl = QtWidgets.QLabel("Results Window")


        self.layout.addWidget(self.tmp_lbl)
        self.setLayout(self.layout)


