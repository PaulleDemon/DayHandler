import sys
import TabHolderWindow

from NotificationScheduler import Notification
from PyQt5 import QtWidgets
from Utils.ThemeController import ThemeController
from Utils.DataBaseOperations import DBHandler


# todo: create Notification, Create a icon

def main():
    DBHandler.initialize_files()

    app = QtWidgets.QApplication(sys.argv)

    ThemeController.register_main_app(app)
    ThemeController.load_theme()

    Notification.load_from_db()

    DBHandler.register("Notification", Notification)

    win = TabHolderWindow.TabbedWidget()
    win.setWindowTitle("Remainder")
    win.show()

    ThemeController.register_icon_class(win)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
