# results_window.py
from PySide2 import QtWidgets, QtCore, QtGui

class ResultsWindow(QtWidgets.QWidget):
    """
    Class for displaying the film results 
    """
    def __init__(self, parent = None):
        super(ResultsWindow, self).__init__(parent)
        print("init results window")
        self.setWindowTitle("Scan Results")
        self.resize(1280, 720)
        self.center_on_screen()
        self.build_gui()

    def center_on_screen(self):
        """
        Center the window on the screen.
        """
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def build_gui(self):
        """
        Init the widgets and layouts to build the gui
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.tmp_lbl = QtWidgets.QLabel("Results Window")


        self.layout.addWidget(self.tmp_lbl)
        self.setLayout(self.layout)


