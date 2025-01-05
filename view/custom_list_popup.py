# custom_list_popup.py

from PySide2 import QtWidgets, QtCore, QtGui

class Custom_List_Popup(QtWidgets.QWidget):
    """
    Class for getting the user's custom list link
    """
    def __init__(self):
        super(Custom_List_Popup, self).__init__()

        self.setWindowTitle("Custom List")
        self.build_gui()

    def build_gui(self):
        """
        Add the needed widgets to the layout
        """
        self.layout = QtWidgets.QVBoxLayout()

        ##############
        ##  WIDGETS ##
        ##############
        self.text_label = QtWidgets.QLabel("Paste the link to your custom list:")
        self.link_line_edit = QtWidgets.QLineEdit()
        self.ok_btn = QtWidgets.QPushButton("Ok")

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.text_label)
        self.main_layout.addWidget(self.link_line_edit)
        self.main_layout.addWidget(self.ok_btn)

        self.layout.addLayout(self.main_layout)
        self.setLayout(self.layout)
