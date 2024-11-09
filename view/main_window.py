# main_window.py

from PySide2 import QtWidgets, QtCore, QtGui

class Main_Window(QtWidgets.QWidget):
    finished_homepageBuild = QtCore.Signal(str)

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


    def build_gui(self):
        """
        Call this function to begin building the base UI
        """
        ##############
        #   WIDGETS  #
        ##############
        self.label = QtWidgets.QLabel("Label")
        self.btn = QtWidgets.QPushButton("Update")

        ##############
        #   LAYOUT   #
        ##############
        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

