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
        self.link.returnPressed.connect(self.startScan)
        self.scanBtn = QtWidgets.QPushButton("Scan List")
        self.scanBtn.clicked.connect(self.startScan)


        # Layouts
        self.layout = QtWidgets.QVBoxLayout()
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

        self.layout.addStretch()
        self.layout.addLayout(self.mainLayout)
        self.layout.addStretch()

        self.setLayout(self.layout)

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
        self.worker_thread.progress_finished.connect(self.loading_popup.close_popup)
        self.worker_thread.progress_finished.connect(self.updateMainWindow)
        self.worker_thread.start()

    def updateMainWindow(self, lbdList, filmDict, servicesList):
        print("DONE SCANNING")
        self.lbdList = lbdList
        self.filmDict = filmDict
        self.servicesList = servicesList
        self.result = FilmResults()
        self.result.show()
        self.hide()

class FilmResults(QtWidgets.QWidget):
    def __init__(self):
        super(FilmResults, self).__init__()
        self.setWindowTitle("Scan Results")
        self.setStyleSheet("color: white; background-color: rgb(30,35,45)")
        self.setGeometry(300, 100, 1280, 720)

        self.initUI()

    def initUI(self):
        ###############
        #   WIDGETS   #
        ###############
        # Side pannel contents
        self.sidePannelLayout = QtWidgets.QVBoxLayout()
        self.streamOrRent = QtWidgets.QLabel("Do you want to Stream or Rent movies :")
        self.streamOrRentSelect = QtWidgets.QComboBox()
        items = ["Stream", "Rent", "Both"]
        self.streamOrRentSelect.addItems(items)
        self.streamOrRentSelect.setCurrentIndex(2)
        self.streamOrRentSelect.currentIndexChanged.connect(self.handleStreamOrRent)

        servicesLayout = QtWidgets.QVBoxLayout()
        servicesLabel = QtWidgets.QLabel("Check your streaming services :")
        servicesLayout.addWidget(servicesLabel)
        self.streamingServicesList = []
        self.selectedServices = []
        current = 0
        for service in widget.servicesList:
            self.currentWidget = QtWidgets.QCheckBox(service)
            self.currentWidget.setChecked(True)
            self.streamingServicesList.append(self.currentWidget)
            servicesLayout.addWidget(self.currentWidget)
            self.currentWidget.stateChanged.connect(self.handleStreamServicesChange)
            self.selectedServices.append(current)
            current += 1
        # Create a scroll area and set its widget to the servicesLayout
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollAreaWidget = QtWidgets.QWidget()
        scrollAreaWidget.setLayout(servicesLayout)
        scrollArea.setWidget(scrollAreaWidget)

        ##############
        #   LAYOUT   #
        ##############
        # Side Pannel Layout
        self.sidePannelGroupBox = QtWidgets.QGroupBox()
        self.leftSidePannel = QtWidgets.QDockWidget()        
        self.leftSidePannel.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.leftSidePannel.setWidget(self.sidePannelGroupBox)
        self.leftSidePannel.show()
        self.sidePannelGroupBox.setLayout(self.sidePannelLayout)
        self.sidePannelLayout.addWidget(self.streamOrRent)
        self.sidePannelLayout.addWidget(self.streamOrRentSelect)
        self.sidePannelLayout.addWidget(scrollArea)

        centerLayout = QtWidgets.QHBoxLayout()
        centerLayout.addWidget(self.leftSidePannel)
        centerLayout.addWidget(QtWidgets.QLabel("Center Layout"))
        centerLayout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(centerLayout)
        self.setLayout(layout)

        self.filmDictVsServices()

    def filmDictVsServices(self):
        '''
        Comparing the checked services and streaming options from the user
        vs the film dict in order to display only what's relevant
        '''
        print("film dict vs services")

    def handleStreamServicesChange(self):
        '''
        Creates a list of indices matching the services selected by the user
        '''
        self.selectedServices = []
        current = 0
        for i in self.streamingServicesList:
            if i.isChecked():
                self.selectedServices.append(current)
            current += 1
        print(self.selectedServices)

    def handleStreamOrRent(self, index):
        selected_item = self.sender().currentText()
        print("Selected Item : %s" % selected_item)


class LoadingPopup(QtWidgets.QDialog):
    def __init__(self):
        super(LoadingPopup, self).__init__()
        self.setStyleSheet("color: white; background-color: rgb(30,35,45)")

        self.setWindowTitle("Comparing your list to JustWatch")
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

    def set_progress(self, value, info):
        self.loading_bar.setValue(value)
        self.movie_label.setText("Scanning : %s" % info)

    def close_popup(self):
        self.accept()

class WorkerThread(QtCore.QThread):
    progress_update = QtCore.pyqtSignal(int, str)
    progress_finished = QtCore.pyqtSignal(list, dict, list)

    def __init__(self, letterBoxLink):
        super(WorkerThread, self).__init__()
        self.letterBoxLink = letterBoxLink

    def run(self):
        lbdList = getList(self.letterBoxLink)

        # Call justwatchCompareGui and let it handle the iteration and progress signals
        filmDict, servicesList = justwatchCompareGui(lbdList, self.progress_update)

        self.progress_finished.emit(lbdList, filmDict, servicesList)  # Emit finished signal when the task is complete


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    widget = LoadingScreen()
    widget.resize(800, 600)
    widget.show()


    sys.exit(app.exec())