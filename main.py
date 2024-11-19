# main.py
import sys
from PySide2 import QtWidgets

from main_controller import Init_main_controller, ResultsController
from model import Init_model
from view.main_window import Main_Window
from view.results_window import ResultsWindow


def main():
    app = QtWidgets.QApplication(sys.argv)

    initModel = Init_model()
    initView = Main_Window()
    Init_main_controller(initModel, initView)
    #initView = ResultsWindow()
    #ResultsController(Init_model, initView)

    initView.resize(1280, 720)
    initView.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
