# main.py
import sys
from PySide2 import QtWidgets

from main_controller import MainController, ResultsController
from model import Init_model
from view.main_window import Main_Window, Loading_Screen

def main():
    app = QtWidgets.QApplication(sys.argv)

    splashcreen = Loading_Screen()

    initModel = Init_model()
    initView = Main_Window()

    MainController(initModel, initView)

    initView.resize(1280, 720)
    initView.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
