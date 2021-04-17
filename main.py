import sys
import Routine

from PyQt5 import QtWidgets
from ImagePaths import ImagePaths
from DataBaseOperations import DBHandler


def main():

    DBHandler.initialize_files()

    app = QtWidgets.QApplication(sys.argv)

    ImagePaths.register_main_app(app)
    ImagePaths.load_theme()

    win = Routine.TabbedWidget()
    win.show()

    ImagePaths.register_icon_class(win)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()


