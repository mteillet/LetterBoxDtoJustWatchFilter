# main_window.py

from PySide2 import QtWidgets, QtCore, QtGui

class Main_Window(QtWidgets.QWidget):
    finished_homepageBuild = QtCore.Signal(str)
    popular_list_signal = QtCore.Signal(str)

    def __init__(self):
        super(Main_Window, self).__init__()
        self.setWindowTitle("LetterBoxD JustWatch Filter")
        #self.build_homepage()

    def build_homepage(self):
        """
        Building the Home page gui
        """
        ##############
        #   WIDGETS  #
        ##############
        self.welcome_lbl = QtWidgets.QLabel("Welcome to the LetterBoxD JustWatch Filter")
        self.languageCbox = QtWidgets.QComboBox()
        self.languageCbox.addItem("French")
        self.languageCbox.addItem("English")
        self.customList_btn = QtWidgets.QPushButton("Use your custom list")
        # https://letterboxd.com/lists/popular/this/week/
        self.popular_lbl = QtWidgets.QLabel("This week's popular categories : ")
        # https://letterboxd.com/search/lists/love+movies/
        self.romance_lbl = QtWidgets.QLabel("Romance Movies :")
        self.horror_lbl = QtWidgets.QLabel("Horror Movies :")
        self.action_lbl = QtWidgets.QLabel("Action Movies :")
        self.comedy_lbl = QtWidgets.QLabel("Comedy Movies :")
        self.thriller_lbl = QtWidgets.QLabel("Thriller Movies :")
        self.animated_lbl = QtWidgets.QLabel("Animated Movies :")
        self.docu_lbl = QtWidgets.QLabel("Documentaries :")
        self.sf_lbl = QtWidgets.QLabel("Science-Fiction Movies :")
        self.biographical_lbl = QtWidgets.QLabel("True Story Movies :")
        self.musical_lbl = QtWidgets.QLabel("Musical Movies :")

        ##############
        #   LAYOUT   #
        ##############
        self.layout = QtWidgets.QVBoxLayout()
        self.topBarLayout = QtWidgets.QHBoxLayout()

        self.popularLayout = QtWidgets.QVBoxLayout()
        self.popularListsLayout = QtWidgets.QHBoxLayout()

        self.categoriesLayout = QtWidgets.QVBoxLayout()
        self.line_1_layout = QtWidgets.QHBoxLayout()
        self.line_2_layout = QtWidgets.QHBoxLayout()
        self.line_3_layout = QtWidgets.QHBoxLayout()
        self.line_4_layout = QtWidgets.QHBoxLayout()
        self.line_5_layout = QtWidgets.QHBoxLayout()

        # Top Bar
        self.layout.addLayout(self.topBarLayout)
        self.topBarLayout.addStretch()
        self.topBarLayout.addWidget(self.welcome_lbl)
        self.topBarLayout.addStretch()
        self.topBarLayout.addWidget(self.languageCbox)
        
        # Custom List
        self.layout.addWidget(self.customList_btn)

        # Popular Movies
        self.layout.addLayout(self.popularLayout)
        self.popularLayout.addWidget(self.popular_lbl)
        self.popularLayout.addLayout(self.popularListsLayout)

        # Categories Layouts
        self.layout.addLayout(self.categoriesLayout)
        self.categoriesLayout.addLayout(self.line_1_layout)
        self.line_1_layout.addWidget(self.romance_lbl)
        self.line_1_layout.addWidget(self.horror_lbl)
        self.categoriesLayout.addLayout(self.line_2_layout)
        self.line_2_layout.addWidget(self.action_lbl)
        self.line_2_layout.addWidget(self.comedy_lbl)
        self.categoriesLayout.addLayout(self.line_3_layout)
        self.line_3_layout.addWidget(self.thriller_lbl)
        self.line_3_layout.addWidget(self.animated_lbl)
        self.categoriesLayout.addLayout(self.line_4_layout)
        self.line_4_layout.addWidget(self.docu_lbl)
        self.line_4_layout.addWidget(self.sf_lbl)
        self.categoriesLayout.addLayout(self.line_5_layout)
        self.line_5_layout.addWidget(self.biographical_lbl)
        self.line_5_layout.addWidget(self.musical_lbl)

        self.setLayout(self.layout)

        self.finished_homepageBuild.emit("Done")

    def add_popular_week(self, filmDict):
        """
        Adds the label and poster of popular this week movie lists
        """

        for key, data in filmDict.items():

            # Posters
            posterSize = QtCore.QSize(70, 105)
            columns = len(data["posters"])
            overlap_amount = 15

            # Final image dimensions
            final_width = columns * posterSize.width() - (columns - 1) * overlap_amount
            final_height = posterSize.height()
            final_pixmap = QtGui.QPixmap(final_width, final_height)
            final_pixmap.fill(QtCore.Qt.white)
            icon = QtGui.QIcon()

            # Painting each poster onto the final image with x-axis overlap
            painter = QtGui.QPainter(final_pixmap)
            x = final_width - posterSize.width()
            for url in data["posters"]:
                poster_image = QtGui.QImage.fromData(url)
                poster_pixmap = QtGui.QPixmap.fromImage(poster_image)
                painter.drawPixmap(x, 0, poster_pixmap)
                x -= posterSize.width() - overlap_amount
            painter.end()
            icon.addPixmap(final_pixmap)

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


