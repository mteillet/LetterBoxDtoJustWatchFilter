# main_window.py

from PySide2 import QtWidgets, QtCore, QtGui

class Main_Window(QtWidgets.QWidget):
    finished_homepageBuild = QtCore.Signal(str)
    popular_list_signal = QtCore.Signal(str)

    def __init__(self):
        super(Main_Window, self).__init__()
        self.setWindowTitle("LetterBoxD JustWatch Filter")
        #self.build_homepage()

    def build_homepage(self, generic_list):
        """
        Building the Home page gui
        """
        ##############
        #   WIDGETS  #
        ##############
        self.welcome_lbl = QtWidgets.QLabel("Welcome to the LetterBoxD JustWatch Filter")
        # Language Combobox
        countries = ["", "", "", "", ""]
        self.languageCbox = QtWidgets.QComboBox()
        self.languageCbox.addItems(countries)
        #self.languageCbox.setEditable(True)
        flags = ["france", "germany", "spain", "united-kingdom", "united-states"]
        current = 0
        for country in countries:
            icon = QtGui.QIcon("./imgs/flags/%s.png" % flags[current])
            self.languageCbox.setItemIcon(current, icon)
            current += 1

        self.customList_btn = QtWidgets.QPushButton("Use your custom list")
        # Popular Lists
        self.popular_lbl = QtWidgets.QLabel("This week's popular categories : ")
        # Classic Lists
        self.classic_lbl = QtWidgets.QLabel("Fit your taste categories :")
        # QScroll Area for these lists
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # Container for the categories layout
        self.scroll_content = QtWidgets.QWidget()
        self.generic_list_btns = []
        for key, valueDicts in generic_list.items():
            icon, final_width, final_height = self.buildPosters(generic_list[key]["posters"])
            self.current_list_btn = MovieListBtn(key, icon, generic_list[key]["link"], final_width, final_height)
            self.current_list_btn.linkSignal.connect(self.popular_signal_emission)
            self.generic_list_btns.append(self.current_list_btn)

        ##############
        #   LAYOUT   #
        ##############
        self.layout = QtWidgets.QVBoxLayout()
        self.topBarLayout = QtWidgets.QHBoxLayout()

        self.popularLayout = QtWidgets.QVBoxLayout()
        self.popularListsLayout = QtWidgets.QHBoxLayout()

        self.categoriesLayout = QtWidgets.QVBoxLayout(self.scroll_content)

        # Top Bar
        self.layout.addLayout(self.topBarLayout)
        self.topBarLayout.addStretch()
        self.topBarLayout.addWidget(self.welcome_lbl)
        self.topBarLayout.addStretch()
        self.topBarLayout.addWidget(self.languageCbox)
        
        # Custom List
        self.layout.addWidget(self.customList_btn)
        self.layout.addWidget(QHLine())

        # Popular Movies
        self.layout.addStretch()
        self.layout.addLayout(self.popularLayout)
        self.popularLayout.addWidget(self.popular_lbl)
        self.popularLayout.addLayout(self.popularListsLayout)
        self.layout.addWidget(QHLine())

        # Categories Layouts
        self.layout.addStretch()
        self.layout.addWidget(self.classic_lbl)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(QHLine())
        self.layout.addStretch()

        # Loop for classic categories layout
        current = 0
        for widget in self.generic_list_btns:
            if current % 3 == 0:
                self.current_cat_layout = QtWidgets.QHBoxLayout()
                self.categoriesLayout.addLayout(self.current_cat_layout)
            self.current_cat_layout.addWidget(widget)
            current += 1

        # Adding them to the container widget
        self.scroll_content.setLayout(self.categoriesLayout)
        self.scroll_area.setWidget(self.scroll_content)

        self.setLayout(self.layout)

        self.finished_homepageBuild.emit("Done")

    def buildPosters(self, posterUrls):
        """
        Building the posters icons
        """
        posterSize = QtCore.QSize(70, 105)
        overlap_amount = 20
        if len(posterUrls) < 10:
            overlap_amount *= 0.5
        columns = len(posterUrls)

        final_width = columns * posterSize.width() - (columns - 1) * overlap_amount
        final_height = posterSize.height()
        final_pixmap = QtGui.QPixmap(final_width, final_height)
        final_pixmap.fill(QtCore.Qt.white)
        icon = QtGui.QIcon()

        painter = QtGui.QPainter(final_pixmap)
        x = final_width - posterSize.width()
        for poster in posterUrls:
            poster_image = QtGui.QImage.fromData(poster)
            #poster_pixmap = QtGui.QPixmap.fromImage(poster_image)
            # Scale the image to fit within posterSize
            poster_pixmap = QtGui.QPixmap.fromImage(poster_image).scaled(posterSize, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        
            painter.drawPixmap(x, 0, poster_pixmap)
            x -= posterSize.width() - overlap_amount
        painter.end()
        icon.addPixmap(final_pixmap)

        return icon, final_width, final_height


    def add_popular_week(self, filmDict):
        """
        Adds the label and poster of popular this week movie lists
        """

        for key, data in filmDict.items():
            icon, final_width, final_height = self.buildPosters(data["posters"])

            # Creating custom widget for the popular lists
            self.popularlist_btn = MovieListBtn(key, icon, data["link"], final_width, final_height)
            # Adding the signal for main controller
            self.popularlist_btn.linkSignal.connect(self.popular_signal_emission)
            # Adding it to the layout 
            self.popularListsLayout.addWidget(self.popularlist_btn)
            self.popularListsLayout.addStretch()

    def popular_signal_emission(self, data):
        """
        Emitting the list link to the main controller
        """
        self.popular_list_signal.emit(data)


class MovieListBtn(QtWidgets.QWidget):
    """
    Custom class for the movies display
    """
    linkSignal = QtCore.Signal(str)
    def __init__(self, text, icon, link, width, height):
        super().__init__()
        self.link = link

        self.styleNotTitle = """
            /* Labels */
            QLabel {
                color: #A0A0A0;
                font-weight: thin;
                font-size: 11px;
            }
            """
        # Set up layout
        layout = QtWidgets.QVBoxLayout()
        
        # Create and set up the icon and text
        self.icon_btn = QtWidgets.QPushButton()
        self.icon_btn.setIcon(icon)
        self.icon_btn.setIconSize(QtCore.QSize(width, height))
        self.icon_btn.clicked.connect(self.emit_link)
        self.icon_btn.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #self.icon_btn.setWidgetResizable(True)
        text_label = QtWidgets.QLabel(text)
        text_label.setStyleSheet(self.styleNotTitle)
        #text_label.setAlignment(QtCore.Qt.AlignCenter)

        # Add icon and text in reverse order for "icon under text"
        layout.addWidget(text_label)
        layout.addWidget(self.icon_btn)

        # Set layout
        self.setLayout(layout)

    def emit_link(self):
        """
        Emitting the link attached to the btn as a signal
        """
        self.linkSignal.emit(self.link)


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


