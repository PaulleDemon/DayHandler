import sys
import TabHolderWindow

from PyQt5 import QtWidgets
from Utils.ThemeController import ThemeController
from Utils.DataBaseOperations import DBHandler


def main():

    DBHandler.initialize_files()

    app = QtWidgets.QApplication(sys.argv)

    ThemeController.register_main_app(app)
    ThemeController.load_theme()

    win = TabHolderWindow.TabbedWidget()
    win.show()

    ThemeController.register_icon_class(win)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()


