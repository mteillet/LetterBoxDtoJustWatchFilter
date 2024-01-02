# letterBoxDtoJwFilter_gui.py
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from backend import getList, justwatchCompareGui

class LoadingScreen(QtWidgets.QWidget):
    '''
    Prompt for entering the LetterBoxD list and displaying loading
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Letter Box D list to Just Watch Availability")
        self.setStyleSheet("color: white; background-color: rgb(30,35,45)")


        # Widgets
        self.title = QtWidgets.QLabel("Paste the link to a LetterBoxD list")
        self.link = QtWidgets.QLineEdit("")
        self.scanBtn = QtWidgets.QPushButton("Scan List")
        self.scanBtn.clicked.connect(self.startScan)


        # Layouts
        layout = QtWidgets.QVBoxLayout()
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.titleLayout = QtWidgets.QHBoxLayout()
        self.linkLayout = QtWidgets.QHBoxLayout()
        self.btnLayout = QtWidgets.QHBoxLayout()

        self.titleLayout.addStretch()
        self.titleLayout.addWidget(self.title)
        self.titleLayout.addStretch()
        self.linkLayout.addWidget(self.link)
        self.btnLayout.addStretch()
        self.btnLayout.addWidget(self.scanBtn)
        self.btnLayout.addStretch()

        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.titleLayout)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.linkLayout)
        self.mainLayout.addStretch
        self.mainLayout.addLayout(self.btnLayout)
        self.mainLayout.addStretch()

        layout.addStretch()
        layout.addLayout(self.mainLayout)
        layout.addStretch()

        self.setLayout(layout)

    ###############################
    # Code for the Slot functions #
    ###############################
    @QtCore.pyqtSlot()
    def startScan(self):
        self.letterBoxLink = self.link.text()
        # Calling loading popup
        self.startPopup()
    
    def startPopup(self):
        # Calling the Loading popup 
        self.loading_popup = LoadingPopup()
        self.loading_popup.show()

        # Connect the progress signal to the set_progress method
        self.worker_thread = WorkerThread(self.letterBoxLink)
        self.worker_thread.progress_update.connect(self.loading_popup.set_progress)
        self.worker_thread.finished.connect(self.loading_popup.close_popup)
        self.worker_thread.start()


class LoadingPopup(QtWidgets.QDialog):
    def __init__(self):
        super(LoadingPopup, self).__init__()
        self.setWindowTitle("Letter Box D list to Just Watch Availability")
        self.setStyleSheet("color: white; background-color: rgb(30,35,45)")

        self.setWindowTitle("Loading Popup")
        self.setGeometry(300, 300, 300, 100)

        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.loading_label = QtWidgets.QLabel("Loading...", self)
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter)
        self.movie_label = QtWidgets.QLabel("", self)
        self.movie_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.loading_label)
        layout.addWidget(self.movie_label)

        self.loading_bar = QtWidgets.QProgressBar(self)
        layout.addWidget(self.loading_bar)

        self.setModal(True)

    def beginScan(self, lbdList):
        #print(lbdList)
        filmDict, servicesList = justwatchCompareGui(lbdList)

    def set_progress(self, value, info):
        self.loading_bar.setValue(value)
        self.movie_label.setText("Scanning : %s" % info)

    def close_popup(self):
        self.accept()

class WorkerThread(QtCore.QThread):
    progress_update = QtCore.pyqtSignal(int, str)

    def __init__(self, letterBoxLink):
        super(WorkerThread, self).__init__()
        self.letterBoxLink = letterBoxLink

    def run(self):
        lbdList = getList(self.letterBoxLink)

        # Call justwatchCompareGui and let it handle the iteration and progress signals
        justwatchCompareGui(lbdList, self.progress_update)

        self.finished.emit()  # Emit finished signal when the task is complete


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    widget = LoadingScreen()
    widget.resize(800, 600)
    widget.show()


    sys.exit(app.exec())