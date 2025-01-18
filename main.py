# main.py
import sys
from PySide2 import QtWidgets

from main_controller import LoadingController, MainController, ResultsController
from model import Init_model
from view.main_window import Main_Window, Loading_Screen

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Splashcreen, initing the base lists models
    splashcreen = Loading_Screen()
    initModel = Init_model()
    loadingController = LoadingController(initModel, splashcreen)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
