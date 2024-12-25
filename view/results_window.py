# results_window.py
from PySide2 import QtWidgets, QtCore, QtGui

class ResultsWindow(QtWidgets.QWidget):
    """
    Class for displaying the film results 
    """
    def __init__(self):
        super(ResultsWindow, self).__init__()
        # print("init results window")
        self.setWindowTitle("Scan Results")
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

        ###############
        ##  WIDGETS  ##
        ###############
        self.list_lbl = QtWidgets.QLabel("List Name")

        # Log viewer
        self.log = QtWidgets.QTextEdit(self)
        self.log.setReadOnly(True)

        # Bottom bar
        self.status_lbl = QtWidgets.QLabel("Scan in progress")
        self.percentage_lbl = QtWidgets.QLabel("{}%".format("50".zfill(2)))
        self.loading_bar = QtWidgets.QLabel("[=====_____]")


        ###############
        ##  LATYOUT  ##
        ###############
        self.log_layout = QtWidgets.QVBoxLayout()
        self.log_layout.addWidget(self.log)

        self.bottom_bar_layout = QtWidgets.QHBoxLayout()
        self.bottom_bar_layout.addStretch()
        self.bottom_bar_layout.addWidget(self.status_lbl)
        self.bottom_bar_layout.addWidget(QVLine())
        self.bottom_bar_layout.addWidget(self.loading_bar)
        self.bottom_bar_layout.addWidget(self.percentage_lbl)

        self.layout.addLayout(self.log_layout)
        self.layout.addWidget(self.list_lbl)
        self.layout.addStretch()
        self.layout.addWidget(QHLine())
        self.layout.addLayout(self.bottom_bar_layout)

        self.setLayout(self.layout)



class QVLine(QtWidgets.QFrame):
    '''
    Simple class to draw separators between the light layouts - VERTICAL
    '''
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class QHLine(QtWidgets.QFrame):
    '''
    Simple class to draw separators between the light layouts - HORIZONTAL
    '''
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


