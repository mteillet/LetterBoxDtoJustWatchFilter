# main.py
import sys
from PySide2 import QtWidgets

from main_controller import Init_main_controller
from model import Init_model
from view.main_window import Main_Window


def main():
    app = QtWidgets.QApplication(sys.argv)

    initModel = Init_model()
    initView = Main_Window()
    Init_main_controller(initModel, initView)

    initView.resize(800, 500)
    initView.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
