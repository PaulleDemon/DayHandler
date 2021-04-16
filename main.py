import sys
import Routine

from PyQt5 import QtWidgets
from ImagePaths import ImagePaths


def load_theme(theme: int):
    global app
    with open(r"Resources/LightTheme.qss") as file:
        theme = file.read()

    ImagePaths.set_theme(1)
    app.setStyleSheet(theme)


def main():
    global app

    app = QtWidgets.QApplication(sys.argv)

    win = Routine.TabbedWidget()
    win.show()

    load_theme(0)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()


