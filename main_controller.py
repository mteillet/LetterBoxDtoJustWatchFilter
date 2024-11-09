# main_controller.py
import re
from time import sleep
import requests
from bs4 import BeautifulSoup

class Init_main_controller():
    def __init__(self, model, view):
        """
        Initializing the main controller with references to the model and view
        """
        self.model = model
        self.view = view
        self.connect_initial_signals()
        # Calling gui build here to get the finish signal
        self.view.build_homepage()
        self.applyStyleSheet()
        #self.connect_signals()

    def connect_initial_signals(self):
        """
        Connecting signals between the model and view before bulding the gui 
        to link right away with the model
        """
        self.view.finished_homepageBuild.connect(self.init_model)

    def init_model(self):
        '''
        Links the model to the corresponding gui widgets
        '''
        print("Signal Received")
        self.get_letterboxd_popular_week()

    def connect_signals(self):
        """
        Connecting signals between the model and view
        """
        print("Connecting Signals")
        # self.view.btn.clicked.connect(lambda: self.updateText())

    def get_letterboxd_popular_week(self):
        """
        Getting letterboxD lists data
        This week's popular categories
        """
        link = "https://letterboxd.com/lists/popular/this/week/"
        page = requests.get(link)

        # Check there was no error getting the list 
        if page.status_code != 200:
            return print("ERROR LOADING THE LINK")

        soup = BeautifulSoup(page.content, features="html.parser")

        print(soup)


    def applyStyleSheet(self):
        stylesheet = """
            /* General Styling */
            QWidget {
                background-color: #1A1A1A;
                color: #FFFFFF;
                font-family: Arial, Helvetica, sans-serif;
            }

            /* Labels */
            QLabel {
                color: #E0E0E0;
                font-size: 14px;
            }

            /* Buttons */
            QPushButton {
                background-color: #333333;
                color: #A3E635;
                padding: 6px 12px;
                border: 1px solid #333333;
                border-radius: 5px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #444444;
                border: 1px solid #A3E635;
            }

            QPushButton:pressed {
                background-color: #555555;
            }

            /* Line Edits */
            QLineEdit {
                background-color: #2A2A2A;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 5px;
                color: #FFFFFF;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #A3E635;
            }

            /* ComboBox */
            QComboBox {
                background-color: #2A2A2A;
                color: #FFFFFF;
                border: 1px solid #444444;
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #444444;
                border-left-style: solid;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }

            QComboBox QAbstractItemView {
                background-color: #2A2A2A;
                selection-background-color: #A3E635;
                selection-color: #1A1A1A;
            }

            /* Text Edits */
            QTextEdit, QPlainTextEdit {
                background-color: #2A2A2A;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 5px;
                color: #FFFFFF;
                font-size: 14px;
            }

            /* Scrollbars */
            QScrollBar:vertical {
                background: #1A1A1A;
                width: 8px;
                margin: 2px 0px 2px 0px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background: #333333;
                min-height: 20px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical:hover {
                background: #444444;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }

            /* GroupBox */
            QGroupBox {
                border: 1px solid #333333;
                border-radius: 5px;
                margin-top: 10px;
                font-size: 14px;
                color: #A3E635;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 2px 5px;
            }

            /* Checkboxes and Radio Buttons */
            QCheckBox, QRadioButton {
                color: #E0E0E0;
                font-size: 14px;
            }

            QCheckBox::indicator, QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 2px;
                background-color: #2A2A2A;
                border: 1px solid #444444;
            }

            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background-color: #A3E635;
                border: 1px solid #A3E635;
            }
            """
        self.view.setStyleSheet(stylesheet)

