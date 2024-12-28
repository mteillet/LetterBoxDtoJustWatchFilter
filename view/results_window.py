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
        # Log viewer
        self.log = QtWidgets.QTextEdit(self)
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(30)

        # Splitter for resizable sections
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitterV = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter_services = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        # Widgets for containing the serivces and movies
        self.services_widget = QtWidgets.QWidget()
        self.services_stream_widget = QtWidgets.QWidget()
        self.services_rent_widget = QtWidgets.QWidget()
        # Widget containing all the different movies scroll areas
        self.films_services_layout_widget = QtWidgets.QWidget()

        # Scroll Areas
        self.services_stream_scroll_area = QtWidgets.QScrollArea()
        self.services_stream_scroll_area.setWidgetResizable(True)
        self.services_rent_scroll_area = QtWidgets.QScrollArea()
        self.services_rent_scroll_area.setWidgetResizable(True)
        self.all_movies_scroll_area = QtWidgets.QScrollArea()
        self.all_movies_scroll_area.setWidgetResizable(True)

        # Scroll area content stream and rent
        self.services_stream_scroll_layout_widget = QtWidgets.QWidget()
        self.services_stream_scroll_layout = QtWidgets.QVBoxLayout(self.services_stream_scroll_layout_widget)
        self.services_stream_scroll_layout_widget.setLayout(self.services_stream_scroll_layout)
        self.services_stream_scroll_area.setWidget(self.services_stream_scroll_layout_widget)
        # Scroll area content all movies 
        self.services_rent_scroll_layout_widget = QtWidgets.QWidget()
        self.services_rent_scroll_layout = QtWidgets.QVBoxLayout(self.services_rent_scroll_layout_widget)
        self.services_rent_scroll_layout_widget.setLayout(self.services_rent_scroll_layout)
        self.services_rent_scroll_area.setWidget(self.services_rent_scroll_layout_widget)
        self.all_movies_scroll_area.setWidget(self.films_services_layout_widget)

        # Bottom bar
        self.status_lbl = QtWidgets.QLabel("Scan in progress")
        self.percentage_lbl = QtWidgets.QLabel("{}%".format("50".zfill(2)))
        self.loading_bar = QtWidgets.QLabel("[__________]")

        ###############
        ##   LAYOUT  ##
        ###############
        self.log_layout = QtWidgets.QVBoxLayout()
        self.log_layout.addWidget(self.log)

        self.bottom_bar_layout = QtWidgets.QHBoxLayout()
        self.bottom_bar_layout.addStretch()
        self.bottom_bar_layout.addWidget(self.status_lbl)
        self.bottom_bar_layout.addWidget(QVLine())
        self.bottom_bar_layout.addWidget(self.loading_bar)
        self.bottom_bar_layout.addWidget(QVLine())
        self.bottom_bar_layout.addWidget(self.percentage_lbl)

        # Splitters Layout
        self.splitter.addWidget(self.log)
        self.splitter.addWidget(self.splitterV)
        # Hiding the log by default
        self.splitter.setSizes([0,200])
        self.layout.addWidget(self.splitter)
        # Splitter services and movies
        self.splitterV.addWidget(self.splitter_services)
        self.splitterV.addWidget(self.all_movies_scroll_area)
        # Splitter Services only
        self.splitter_services.addWidget(self.services_stream_widget)
        self.splitter_services.addWidget(self.services_rent_widget)
        self.splitter_services.setSizes([75,25])

        # Layout for services list
        self.services_stream_lay = QtWidgets.QVBoxLayout(self.services_stream_widget)
        self.services_stream_lay.addWidget(QtWidgets.QLabel("Streaming Services:"))
        self.services_stream_lay.addWidget(self.services_stream_scroll_area)
        self.services_rent_lay = QtWidgets.QVBoxLayout(self.services_rent_widget)
        self.services_rent_lay.addWidget(QtWidgets.QLabel("Renting Services:"))
        self.services_rent_lay.addWidget(self.services_rent_scroll_area)

        # Layout for movies
        self.films_services_layout = QtWidgets.QVBoxLayout(self.films_services_layout_widget)

        # self.layout.addStretch()
        self.layout.addWidget(QHLine())
        self.layout.addLayout(self.bottom_bar_layout)

        self.setLayout(self.layout)

    def create_service_stream_radio_button(self, data):
        """
        Create a radio button for a new service, and add it to the services_stream_scroll_layout
        """
        new_button = QtWidgets.QRadioButton(data)
        self.services_stream_scroll_layout.addWidget(new_button)

    def create_service_rent_radio_button(self, data):
        """
        Create a radio button for a new service, and add it to the services_rent_scroll_layout
        """
        new_button = QtWidgets.QRadioButton(data)
        self.services_rent_scroll_layout.addWidget(new_button)

    def create_service_movies_layout(self, data):
        """
        Creating necessary scroll area and layout to be able to add movies to it
        """
        service_movie_scroll_area = QtWidgets.QScrollArea()
        service_movie_scroll_area.setWidgetResizable(True)
        service_movie_scroll_area.setMinimumHeight(240)
        service_movie_scroll_widget = QtWidgets.QWidget()
        service_movie_scroll_layout = QtWidgets.QHBoxLayout(service_movie_scroll_widget)
        service_movie_scroll_widget.setLayout(service_movie_scroll_layout)
        service_movie_scroll_area.setWidget(service_movie_scroll_widget)

        # Setting up a label widget to show the service name for clarity
        service_label = QtWidgets.QLabel(data)

        # Adding title of the service before the scrollbar
        self.films_services_layout.addWidget(service_label)
        self.films_services_layout.addWidget(service_movie_scroll_area)

        return {"name" : data, "layout" : service_movie_scroll_layout, "label" : service_label}

    def add_movie_to_service_layout(self, movie, poster, layout):
        """
        Adding a movie to its corresponding streaming service layout
        """
        # TO DO 
        # Need to setup custom QPushButtons widgets, with the movie title
        # The movie poster, and needs to open the url link when the button is clicked
        posterSize = QtCore.QSize(140, 210)
        poster_image = QtGui.QImage.fromData(poster)
        poster_pixmap = QtGui.QPixmap.fromImage(poster_image).scaled(posterSize, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        movie_widget = QtWidgets.QLabel(movie)
        movie_widget.setPixmap(poster_pixmap)
        layout.addWidget(movie_widget)


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


