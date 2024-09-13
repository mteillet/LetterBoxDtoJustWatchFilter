# letterBoxDtoJwFilter_gui.py
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import requests
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
        print(lbdList)
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
            self.currentWidget.setChecked(False)
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
        self.leftSidePannel.setFixedWidth(300)
        self.leftSidePannel.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.leftSidePannel.setWidget(self.sidePannelGroupBox)
        self.leftSidePannel.show()
        self.sidePannelGroupBox.setLayout(self.sidePannelLayout)
        self.sidePannelLayout.addWidget(self.streamOrRent)
        self.sidePannelLayout.addWidget(self.streamOrRentSelect)
        self.sidePannelLayout.addWidget(scrollArea)

        self.centerLayout = QtWidgets.QHBoxLayout()
        self.centerLayout.addWidget(self.leftSidePannel)
        #self.centerLayout.addWidget(QtWidgets.QLabel("Center Layout"))
        #self.centerLayout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(self.centerLayout)
        self.setLayout(layout)

        self.filmDictVsServices()

    def filmDictVsServices(self):
        '''
        Comparing the checked services and streaming options from the user
        vs the film dict in order to display only what's relevant
        '''
        streamOrRentSelection = self.checkStreamOrRent()
        streamingDict = {}
        rentingDict = {}

        for i in self.selectedServices:
            # Retrieve Streaming service name
            streamService = self.streamingServicesList[int(i)].text()
            if streamOrRentSelection == "Stream" or streamOrRentSelection == "Both":
                streamingDict[streamService] = []
                for film in widget.filmDict:
                    try:
                        if streamService in widget.filmDict[film]["streaming"]:
                            #print("%s found for movie : %s" % (streamService, widget.filmDict[film]["jwTitle"]))
                            streamingDict[streamService].append(widget.filmDict[film]["jwTitle"])
                    except KeyError:
                        print("Error for movie : %s and streaming service %s" % (film, streamService))
            if streamOrRentSelection == "Rent" or streamOrRentSelection == "Both":
                rentingDict[streamService] = []
                for film in widget.filmDict:
                    try:
                        if streamService in widget.filmDict[film]["rent"]:
                            #print("%s found for movie : %s" % (streamService, widget.filmDict[film]["jwTitle"]))
                            rentingDict[streamService].append(widget.filmDict[film]["jwTitle"])
                    except KeyError:
                        print("Error for movie : %s and renting service %s" % (film, streamService))

        # For debugging purposes
        self.cliDebugResults(streamingDict, rentingDict)
        print(widget.filmDict)

        # Build UI widgets using the streaming and renting Dict
        self.buildFilmUI(streamingDict, rentingDict)

    def cliDebugResults(self, streamingDict, rentingDict):
        '''
        Use for debugging purposes, will print the fetched results
        '''
        for platform in streamingDict:
            print("The following are available on %s" % platform)
            for movie in streamingDict[platform]:
                print(" -- %s" % movie)
        for platform in rentingDict:
            print("The following are available on %s" % platform)
            for movie in rentingDict[platform]:
                print(" -- %s" % movie)

    def buildFilmUI(self, streamingDict, rentingDict):
        '''
        Responsible for building the film and found services UI
        '''
        # Check if the attribute exists
        if hasattr(self, "allMoviesContainerLayout"):
            # Clear the layout if it exists
            self.clearLayout(self.allMoviesContainerLayout)
        # Looping over the films contained in the streamingDict
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        boldFont.setPointSize(15)
        self.allServicesLayout = QtWidgets.QVBoxLayout()
        self.allMoviesContainerLayout = QtWidgets.QVBoxLayout()

        # Streaming dict
        for service in streamingDict:
            # If list associated to service is not empty
            if streamingDict[service] and service != "None":
                currentServiceLayout = QtWidgets.QVBoxLayout()
                serviceLabel = QtWidgets.QLabel("%s Streaming:" % service)
                serviceLabel.setFont(boldFont)
                serviceNameLayout = QtWidgets.QHBoxLayout()
                serviceNameLayout.addWidget(serviceLabel)
                serviceNameLayout.addStretch()

                # Movies contained in service
                moviesLayout = QtWidgets.QHBoxLayout()
                # Scrolling through the films
                scrollMovieArea = QtWidgets.QScrollArea()
                scrollMovieArea.setWidgetResizable(True)
                scrollMovieAreaWidget = QtWidgets.QWidget()
                for movie in streamingDict[service]:
                    posterLayout = QtWidgets.QVBoxLayout()
                    movieName = QtWidgets.QLabel(movie)
                    movieName.setAlignment(QtCore.Qt.AlignCenter)
                    movieImage = QtWidgets.QLabel(movie)
                    movieImage.setAlignment(QtCore.Qt.AlignCenter)
                    for film in widget.filmDict:
                        if widget.filmDict[film]["jwTitle"] == movie:
                            image_data = widget.filmDict[film]["poster"]
                            # Get the image data from the URL
                            image = QtGui.QImage.fromData(image_data)
                            pixmap = QtGui.QPixmap.fromImage(image)
                            movieImage.setPixmap(pixmap)
                    posterLayout.addWidget(movieImage)
                    posterLayout.addWidget(movieName)
                    moviesLayout.addLayout(posterLayout)
                    moviesLayout.addWidget(QVLine())
                moviesLayout.addStretch()
                scrollMovieAreaWidget.setLayout(moviesLayout)
                scrollMovieArea.setWidget(scrollMovieAreaWidget)
                scrollMovieArea.setMinimumHeight(300)
                currentServiceLayout.addLayout(serviceNameLayout)
                currentServiceLayout.addWidget(scrollMovieArea)
                currentServiceLayout.addWidget(QHLine())
                # Adding the current service layout to a layout containing all of them
                self.allServicesLayout.addLayout(currentServiceLayout)

        for service in rentingDict:
            # Making sure list is not empty
            if rentingDict[service] and service != "None":
                currentServiceLayout = QtWidgets.QVBoxLayout()
                serviceLabel = QtWidgets.QLabel("%s Renting:" % service)
                serviceLabel.setFont(boldFont)
                serviceNameLayout = QtWidgets.QHBoxLayout()
                serviceNameLayout.addWidget(serviceLabel)
                serviceNameLayout.addStretch()

                # Movies contained in service
                moviesLayout = QtWidgets.QHBoxLayout()
                # Scrolling through the films
                scrollMovieArea = QtWidgets.QScrollArea()
                scrollMovieArea.setWidgetResizable(True)
                scrollMovieAreaWidget = QtWidgets.QWidget()
                for movie in rentingDict[service]:
                    posterLayout = QtWidgets.QVBoxLayout()
                    movieName = QtWidgets.QLabel(movie)
                    movieName.setAlignment(QtCore.Qt.AlignCenter)
                    movieImage = QtWidgets.QLabel(movie)
                    movieImage.setAlignment(QtCore.Qt.AlignCenter)
                    for film in widget.filmDict:
                        if widget.filmDict[film]["jwTitle"] == movie:
                            image_data = widget.filmDict[film]["poster"]
                            # Get the image data from the URL
                            image = QtGui.QImage.fromData(image_data)
                            pixmap = QtGui.QPixmap.fromImage(image)
                            movieImage.setPixmap(pixmap)
                    posterLayout.addWidget(movieImage)
                    posterLayout.addWidget(movieName)
                    moviesLayout.addLayout(posterLayout)
                    moviesLayout.addWidget(QVLine())
                moviesLayout.addStretch()
                scrollMovieAreaWidget.setLayout(moviesLayout)
                scrollMovieArea.setWidget(scrollMovieAreaWidget)
                scrollMovieArea.setMinimumHeight(300)
                currentServiceLayout.addLayout(serviceNameLayout)
                currentServiceLayout.addWidget(scrollMovieArea)
                currentServiceLayout.addWidget(QHLine())
                # Adding the current service layout to a layout containing all of them
                self.allServicesLayout.addLayout(currentServiceLayout)

        self.allServicesLayout.addStretch()

        # Adding the build blocks to the self.centerLayout
        scrollAllMovies = QtWidgets.QScrollArea()
        scrollAllMoviesWidget = QtWidgets.QWidget()
        scrollAllMoviesWidget.setLayout(self.allServicesLayout)
        scrollAllMovies.setWidget(scrollAllMoviesWidget)
        scrollAllMovies.setWidgetResizable(True)
        # Adding the widget to a layout
        self.allMoviesContainerLayout.addWidget(scrollAllMovies)
        self.centerLayout.addLayout(self.allMoviesContainerLayout)

    def clearLayout(self, layout):
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    #widget.setParent(None)
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())
                    #sublayout = item.layout()
                    #if sublayout:
                    #    self.clearLayout(sublayout)

    def checkStreamOrRent(self):
        '''
        Returns if the user chose to stream, rent, or both
        '''
        return(self.streamOrRentSelect.currentText())

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

        #print(self.selectedServices)
        self.filmDictVsServices()

    def handleStreamOrRent(self, index):
        selected_item = self.sender().currentText()
        #print("Selected Item : %s" % selected_item)
        self.filmDictVsServices()


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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    widget = LoadingScreen()
    widget.resize(800, 600)
    widget.show()


    sys.exit(app.exec())
